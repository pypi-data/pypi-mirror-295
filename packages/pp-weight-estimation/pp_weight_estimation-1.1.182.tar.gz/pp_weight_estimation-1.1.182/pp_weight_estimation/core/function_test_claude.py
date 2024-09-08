from PIL import Image
import os
import pandas as pd
from mb_utils.src import logging
from pp_weight_estimation.utils.slack_connect import send_message_to_slack
from pp_weight_estimation.core.get_weight import  get_histogram, get_val, split_filename
from pp_weight_estimation.core.s3_io import  download_image,get_response
from pp_weight_estimation.core.gpt_support import get_count,multi_ref_prompt_claude,get_claude_result,get_claude_result2,get_claude_count
from typing import List,Union
import yaml
import boto3
from datetime import datetime
from tqdm import tqdm
import numpy as np
import cv2
import ast
import shutil
import time


def load_config(yaml_path: str) -> dict:
    """
    Function to load configurations from a YAML file
    Args:
        yaml_path (str): Path to the YAML file
    Returns:
        dict: Dictionary containing configurations
    """
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def process_pipeline_new(config_path: str, logger: logging.Logger = None, **kwargs) -> Union[pd.DataFrame, List]:
    """
    Function to process the pipeline of Production Planning.
    
    This function automates the process of downloading images from an S3 bucket, applying segmentation and masking,
    calculating histograms, and saving the results to an output CSV file. The function uses configurations provided
    in a YAML file for flexibility.

    Args:
        config_path (str): Path to the YAML configuration file.
        logger (logging.Logger): Logger object for logging messages (optional).
        **kwargs: Additional keyword arguments (optional).
        
    Returns:
        tuple: A tuple containing:
            - str: The path to the output CSV file.
            - list: A list of results for each processed image.
    """
    config = load_config(config_path)

    input_csv_path = config['data']['input_csv_path']
    input_csv_limit = config['data'].get('limit', None)

    replace_images = config['data'].get('replace_images', False)
    path_to_save_images = config['data']['path_to_save_images']
    if path_to_save_images[-1] != '/':
        path_to_save_images += '/'
    annotation_data_res = config['data'].get('annotation_data_res', False)
    gpt_best_image = config['data'].get('gpt_best_image', False)
    resize_for_multi_ref = config['data'].get('resize_for_multi_ref', False)

    slack_post = config['results'].get('slack_post', False)
    slack_webhook = config['results'].get('slack_webhook', None)

    bucket = config['aws_data']['bucket_name']
    profile = config['aws_data']['profile']

    # gpt_response = config['gpt_res'].get('gpt_response', False)
    # gpt_prompt = config['gpt_res'].get('gpt_prompt', None)
    # gpt_api_key = config['gpt_res']['gpt_api_key']

    claude_api_key = config['claude_res']['gpt_api_key']
    claude_response = config['claude_res'].get('claude_response', False)

    claude_prompt_multi= config['claude_res'].get('claude_prompt_multi', None)

    output_file_name = config['data'].get('output_file_name', None)
    todays_date = "{:%Y_%m_%d}".format(datetime.now())

    session = boto3.Session()
    client = session.client(profile)


    # groundtruth_df = pd.read_csv(gt_csv_path)
    input_df = pd.read_csv(input_csv_path)
    if input_csv_limit is not None:
        input_df = input_df[:input_csv_limit]
    if logger:
        logger.info("Length of input dataframe: {}".format(len(input_df)))
    error_reference_path_index = input_df[input_df.s3_reference_image_path.str.startswith('site/')].index
    input_df = input_df.drop(error_reference_path_index).reset_index(drop=True)
    if logger:
        logger.info("Dropping reference image path with site/ prefix : {}".format(error_reference_path_index))
        logger.info("Length of input dataframe after dropping reference image path with site/ prefix: {}".format(len(input_df)))
    input_df = input_df[input_df['s3_image_path'].notna()]
    input_df = input_df[input_df['s3_reference_image_path'].notna()]
    input_df.reset_index(drop=True, inplace=True)
    if logger:
        logger.info("Length of input dataframe after removing null values: {}".format(len(input_df)))
        
    # input_df['ground_truth_g']=input_df['ground_truth_kg']*1000
    input_df['rework_g']=input_df['rework_kg']*1000
    
    if gpt_best_image:
        input_df['gpt_best_image'] = 0.0
        input_df['gpt_best_success'] = False
    if annotation_data_res:
        input_df['annotation_result'] = 0.0
        input_df['annotation_error'] = 0.0
        input_df['annotation_success'] = False
    if claude_response:
        input_df['gpt_result'] = 0.0
        input_df['gpt_error'] = 0.0
        input_df['gpt_success'] = False
        input_df['gpt_count_res'] = False
        input_df['gpt_count_value'] = 0.0

    #use_input_groundtruth = 'input_groundtruth' in input_df.columns

    input_view_image_bb=[]
    input_view_image_mask=[]
    ref_view_image_bb=[]
    ref_view_image_mask=[]

    entries = []
    for val_num, row in input_df.iterrows():
        replace_images=True
        bucket= 'pp-image-capture-processed-useast1-prod'
        path_to_save_images = '/data/pp_data_new/'
        s3_image_path = row['s3_image_path']
        image_dict = split_filename(row['s3_image_path'])
        local_image_folder = path_to_save_images + image_dict['site_id'] + '/' + image_dict['food_item'] + '/'
        os.makedirs(local_image_folder, exist_ok=True)
        local_image_path = path_to_save_images + image_dict['site_id'] + '/' + image_dict['food_item'] + '/' + image_dict['image'] + '.jpeg'
        if os.path.exists(local_image_path) and replace_images is False:
            # if logger:
            #     logger.info(f"Image {local_image_path} already exists. Skipping download.")   
            pass
        else:
            img_temp = download_image(bucket, row['s3_image_path'], client)
            img_temp.save(local_image_path)
        site_id = image_dict['site_id']
        #taxonomy_code = row['taxonomy_code']
        food_item = image_dict['food_item']
        #input_groundtruth = row['input_groundtruth'] if use_input_groundtruth else 0

        food_item_label = row['food_item_label']
        # try:
            # s3_reference_image_path = eval(row['s3_reference_image_path'])
        # except:
        #     s3_reference_image_path = row['s3_reference_image_path']
        temp_s3_reference_image_path = row['s3_reference_image_path']
        new_ref_list = []
        # print((isinstance(temp_s3_reference_image_path,list)))
        # stop
        print(f'STARTING LOOP : {val_num}')
        if len(temp_s3_reference_image_path)>164:
            ref_list = ast.literal_eval(temp_s3_reference_image_path)
            print(f'ref_list: {ref_list}')
            for i in ref_list:
                ref_dict = split_filename(i)
                local_image_folder_ref = path_to_save_images + ref_dict['site_id'] + '/' + ref_dict['food_item'] + '/'
                os.makedirs(local_image_folder_ref, exist_ok=True)
                local_image_path_ref = path_to_save_images + ref_dict['site_id'] + '/' + ref_dict['food_item'] + '/' + ref_dict['image'] + '.jpeg'
                if os.path.exists(local_image_path_ref) and replace_images is False:
                    pass
                else:
                    img_temp = download_image(bucket, i, client)
                    img_temp.save(local_image_path_ref)
                new_ref_list.append(local_image_path_ref)
            # s3_reference_image_path = eval(row['s3_reference_image_path']) ## making every reference image path as list
        else:
            s3_reference_image_path_ori = row['s3_reference_image_path']
            print(f's3_path_check_download_loop: {s3_reference_image_path_ori}')
            temp_s3_ref = split_filename(s3_reference_image_path_ori)
            local_image_folder_ref2 = path_to_save_images + temp_s3_ref['site_id'] + '/' + temp_s3_ref['food_item'] + '/'
            os.makedirs(local_image_folder_ref2, exist_ok=True)
            local_image_path_ref2 = path_to_save_images + temp_s3_ref['site_id'] + '/' + temp_s3_ref['food_item'] + '/' + temp_s3_ref['image'] + '.jpeg'
            if os.path.exists(local_image_path_ref2) and replace_images is False:
                pass
            else:
                print(s3_reference_image_path_ori)
                img_temp = download_image(bucket, s3_reference_image_path_ori, client)
                img_temp.save(local_image_path_ref2)
            new_ref_list.append(local_image_path_ref2)
    
        # print(f'new_ref_list: {new_ref_list}')
        try:
            s3_reference_weight = ast.literal_eval(row['ground_truth_kg'])
        except:
            s3_reference_weight = row['ground_truth_kg']
        if isinstance(s3_reference_weight,list):
            s3_reference_weight = [x*1000 for x in s3_reference_weight]
            rework_g = row['rework_kg']*1000
        else:
            s3_reference_weight = s3_reference_weight*1000
            rework_g = row['rework_kg']*1000

        if new_ref_list is None:
            if logger:
                logger.error(f"No reference image found for image {local_image_path}. Skipping image.")
        else:
            print(f's3_path_check: {new_ref_list}')

            if len(new_ref_list) > 1:
                print(f'Processing multi reference image for {local_image_path}')
                if claude_prompt_multi is None:
                    prompt_multi_ref = "I want you to act like a Food Image Search Assistant. Which image is the most similar to the Base image? PLEASE JUST respond with dictonary {'image': value}. Base Image: " 
                else:
                    prompt_multi_ref = claude_prompt_multi
                if resize_for_multi_ref:
                    dir = './resized_temp/'
                    if os.path.exists(dir):
                        shutil.rmtree(dir)
                    os.makedirs(dir,exist_ok=True)
                    local_image_path_resize = cv2.resize(np.array(Image.open(local_image_path)),(512,512))  ## resize the image to 512x512  
                    cv2.imwrite('./resized_temp/' + image_dict['image'] + '.jpeg',local_image_path_resize)
                    for i in range(len(new_ref_list)):
                        local_image_path_ref_resize = cv2.resize(np.array(Image.open(new_ref_list[i])),(512,512))
                        cv2.imwrite('./resized_temp/' + split_filename(new_ref_list[i])['image'] + '.jpeg',local_image_path_ref_resize)
                    new_ref_list_updated = ['./resized_temp/' + split_filename(new_ref_list[i])['image'] + '.jpeg' for i in range(len(new_ref_list))]
                    local_image_path_updated = './resized_temp/' + image_dict['image'] + '.jpeg'
                    multi_ref_res = multi_ref_prompt_claude(local_image_path_updated, new_ref_list_updated, prompt=prompt_multi_ref, api_key=claude_api_key)
                else:
                    multi_ref_res = multi_ref_prompt_claude(local_image_path, new_ref_list, prompt=prompt_multi_ref, api_key=claude_api_key)
                print(f'multi_ref_res image : {multi_ref_res}')
                time.sleep(30)
                if multi_ref_res:
                    multi_ref_res = eval(multi_ref_res)
                    multi_ref_res_image = multi_ref_res['image']
                    val_for_list = multi_ref_res_image-1
                    s3_reference_weight = s3_reference_weight[val_for_list]
                    # print(f's3_reference_weight : {s3_reference_weight}')
                    s3_reference_image_path = new_ref_list[val_for_list]
                    s3_reference_image_path_ori = ref_list[val_for_list]
                    input_df.at[val_num, 'gpt_best_image'] = val_for_list
                    input_df.at[val_num, 'gpt_best_success'] = True
                else:
                    if logger:
                        logger.error(f"Error processing list input {local_image_path}")
            else:
                s3_reference_image_path = new_ref_list[0]
                s3_reference_image_path_ori = ref_list[0]
                s3_reference_weight = s3_reference_weight[0]

            print(f's3_reference_path_local : {s3_reference_image_path}')
            print(f's3_reference_image_path_ori : {s3_reference_image_path_ori}')
            print(f'reference_weight : {s3_reference_weight}')
            print(f's3_image_path : {s3_image_path}')
            if local_image_path and site_id and food_item:
                #composed_key = f"{site_id}_{taxonomy_code}"
                entries.append((site_id, local_image_path, food_item,local_image_folder,image_dict['image'],s3_image_path,s3_reference_image_path_ori,
                                s3_reference_image_path,s3_reference_weight,rework_g,food_item_label))
                ##write entries to csv
                new_csv = pd.DataFrame(entries,columns=['site_id','local_image_path','food_item','local_image_folder','image_dict_name','s3_image_path',
                                                        'reference_image_s3','reference_image','reference_image_gt','rework_g','food_item_label'])
                new_csv.to_csv('./temp_entries.csv',index=False)

    if not entries:
        if logger:
            logger.error("No valid entries found in the CSV file")
        raise ValueError("No valid entries found in the CSV file")
    
    #results = []
    for index, (site_id, local_image_path, food_item,local_image_folder,image_dict_name,s3_image_path,reference_image_s3,reference_image,reference_image_gt,rework_g,
                food_item_label) in enumerate(tqdm(entries, desc="Processing images",leave=False)):
        
        if annotation_data_res:
            main_image_dict = {}
            main_image_dict['bb_path'] ='labelbox/' + s3_image_path[:-13] + '/bounding_box.json'
            main_image_dict['mask_path'] = 'labelbox/' + s3_image_path[:-13] + '/mask.jpg'
            ref_image_dict = {}
            ref_image_dict['bb_path'] ='labelbox/' + reference_image_s3[:-13] + '/bounding_box.json'
            ref_image_dict['mask_path'] = 'labelbox/' + reference_image_s3[:-13] + '/mask.jpg'
            # print(main_image_dict)
            # print(ref_image_dict)
            labelbox_bucket='pp-image-weight-estimation-euwest1-uat'

            var_img=False
            var_ref_img=False
            try:
                if main_image_dict['bb_path'] is not None:
                    client.get_object(Bucket=labelbox_bucket, Key=main_image_dict['bb_path'])
                    client.get_object(Bucket=labelbox_bucket, Key=main_image_dict['mask_path'])
                    var_img=True
            except:
                if logger:
                    logger.error(f"Error downloading annotation data for image {s3_image_path}")
            
            try:
                if ref_image_dict['bb_path'] is not None:
                    client.get_object(Bucket=labelbox_bucket, Key=ref_image_dict['bb_path'])
                    client.get_object(Bucket=labelbox_bucket, Key=ref_image_dict['mask_path'])
                    var_ref_img=True
            except:
                if logger:
                    logger.error(f"Error downloading annotation data for ref image {ref_image_dict['bb_path']}")

            if var_img and var_ref_img:
                try:
                    main_image_s3_bb = get_response(client,labelbox_bucket,main_image_dict['bb_path'])
                    main_image_bb = eval(main_image_s3_bb['Body'].read().decode('utf-8'))
                    main_image_mask = download_image(labelbox_bucket,main_image_dict['mask_path'],client)
                    main_image_mask.save(local_image_folder + image_dict_name + "_annotation_mask.jpeg")

                    ref_image_s3_bb = get_response(client,labelbox_bucket,ref_image_dict['bb_path'])
                    ref_image_bb = eval(ref_image_s3_bb['Body'].read().decode('utf-8'))
                    ref_image_mask = download_image(labelbox_bucket,ref_image_dict['mask_path'],client)

                    x1_bb,y1_bb,x2_bb,y2_bb  = int(main_image_bb['top']),int(main_image_bb['left']),int(main_image_bb['height']),int(main_image_bb['width'])
                    x1_ref_bb,y1_ref_bb,x2_ref_bb,y2_ref_bb  = int(ref_image_bb['top']),int(ref_image_bb['left']),int(ref_image_bb['height']),int(ref_image_bb['width'])

                    image_data = np.array(Image.open(local_image_path))
                    mask_data = np.array(main_image_mask)
                    bbox_image = image_data[x1_bb:(x2_bb+x1_bb),y1_bb:(y2_bb+y1_bb)]
                    bbox_mask = mask_data[x1_bb:(x2_bb+x1_bb),y1_bb:(y2_bb+y1_bb)]
                    bbox_image2 = cv2.resize(bbox_image, (512,512))
                    bbox_mask2 = cv2.resize(bbox_mask, (512,512))

                    ref_image_data = np.array(Image.open(reference_image))
                    ref_mask_data = np.array(ref_image_mask)
                    ref_bbox_image = ref_image_data[x1_ref_bb:(x2_ref_bb+x1_ref_bb),y1_ref_bb:(y2_ref_bb+y1_ref_bb)]
                    ref_bbox_mask = ref_mask_data[x1_ref_bb:(x2_ref_bb+x1_ref_bb),y1_ref_bb:(y2_ref_bb+y1_ref_bb)]
                    ref_bbox_image2 = cv2.resize(ref_bbox_image, (512,512))
                    ref_bbox_mask2 = cv2.resize(ref_bbox_mask, (512,512))
        
                    hist_mask,_ = get_histogram(bbox_mask2)
                    hist_ref_mask,_ = get_histogram(ref_bbox_mask2)
                    # print(hist_mask[-1])
                    # print(hist_ref_mask[-1])
                    img_weight,img_error = get_val(hist_ref_mask[-1],hist_mask[-1],reference_image_gt,rework_g)

                    input_df.at[index, 'annotaion_result']  = round(img_weight,2)
                    input_df.at[index, 'annotation_error'] =  round(img_error,2)
                    input_df.at[index, 'annotation_success'] = True

                    input_view_image_bb.append(bbox_image2)
                    input_view_image_mask.append(bbox_mask2)
                    ref_view_image_bb.append(ref_bbox_image2)
                    ref_view_image_mask.append(ref_bbox_mask2)

                except Exception as e:
                    if logger:
                        logger.error(f"Error processing annotation data for image {s3_image_path}")
                    input_df.at[index, 'annotation_success'] = False
                    input_df.at[index, 'annotation_error'] = 0.0
                    input_df.at[index, 'annotation_result'] = 0.0
            else:
                input_df.at[index, 'annotation_success'] = False
                input_df.at[index, 'annotation_error'] = 0.0
                input_df.at[index, 'annotation_result'] = 0.0

        if claude_response:
            gpt_prompt = f"Based on the reference image of weight {food_item_label} : {reference_image_gt} grams, what is the weight of the 2nd image? Please respond only in the format 'amount' without grams unit."
            try:
                # print(f'local_image_path : {local_image_path}')
                # print(f'reference_image_s3 : {reference_image}')
                gpt_result = get_claude_result(image_path = local_image_path, ref_image_path= reference_image, api_key = claude_api_key, prompt = gpt_prompt)
                # print(f'gpt_refernece prompt gpt_res : {gpt_result}')
                gpt_final_result = get_claude_count(gpt_result) 
            except:
                gpt_final_result = False

            if gpt_final_result!=False:
                try:
                    gpt_error = (abs(rework_g-gpt_final_result)/rework_g)*100 if rework_g !=0 else 0.0
                    input_df.at[index, 'gpt_success'] = True 
                    print(f'gpt_error for {food_item_label}: {gpt_error}')
                except:
                    gpt_error = 0.0
                    input_df.at[index, 'gpt_success'] = False
            else:
                gpt_error = 0.0
                input_df.at[index, 'gpt_success'] = False
            input_df.at[index, 'gpt_error'] = gpt_error
            print(f'gpt_result for {food_item_label}: {gpt_final_result}')
            input_df.at[index, 'gpt_result'] = gpt_final_result
        
            gpt_prompt2 = f"If the {food_item_label} item can be counted. Please respond only the count in the format 'amount' and if it cannot be counted respond 'False'."
            try:
                gpt_result2 = get_claude_result2(image_path = local_image_path, api_key = claude_api_key, prompt = gpt_prompt2)
                # print(f"gpt_result2: {gpt_result2}")
                gpt_final_result2 = get_claude_count(gpt_result2) 
                # print(f"gpt_result2 after get_count: {gpt_final_result2}")
            except:
                gpt_final_result2 = False

            if gpt_final_result2!=False:
                gpt_count_value = gpt_final_result2
                input_df.at[index, 'gpt_count_res'] = True
                # try:
                #     input_df.at[index, 'gpt_count_res'] = True 
                #     #print(f'gpt_count for {food_item_label}: {gpt_final_result2}')
                # except Exception as e:
                #     gpt_count_value = 0.0
                #     input_df.at[index, 'gpt_count_res'] = False
            else:
                gpt_count_value = 0.0
                input_df.at[index, 'gpt_count_res'] = False
            input_df.at[index, 'gpt_count_value'] = gpt_count_value
            print(f'gpt_count for {food_item_label}: {gpt_count_value}')
    
    output_csv_dir = path_to_save_images + 'output_csv/'
    os.makedirs(output_csv_dir, exist_ok=True)
    if output_file_name is not None:
        output_csv_path = os.path.join(output_csv_dir, output_file_name)
    else:
        output_csv_path = os.path.join(output_csv_dir, f"output_{todays_date}.csv")
    input_df.to_csv(output_csv_path, index=False)

    if logger:
        logger.info(f"Processing complete. Output saved to {output_csv_path}")

    try:
        temp_pd = input_df[['site_id','food_item_label','rework_g']]
        if annotation_data_res:
            temp_pd['annotation_result'] = input_df['annotation_result']
            temp_pd['annotation_error'] = input_df['annotation_error']
            temp_pd['annotation_success'] = input_df['annotation_success']

        if claude_response:
            temp_pd['gpt_result'] = input_df['gpt_result']
            temp_pd['gpt_error'] = input_df['gpt_error']
            temp_pd['gpt_count_value'] = input_df['gpt_count_value']
            temp_pd['gpt_count_res'] = input_df['gpt_count_res']
    except Exception as e:
        if logger:
            logger.error(f"Error sending message to slack: {e}")
    
    if slack_post:
        send_message_to_slack(temp_pd, is_df=True,url=slack_webhook,tabulate_type='fancy_grid')

    return input_df,temp_pd,input_view_image_bb,input_view_image_mask,ref_view_image_bb,ref_view_image_mask
    #return output_csv_path, results