def check_posted_data(posted_data, function_name=None):
    
    if "x" not in posted_data or "y" not in posted_data:
        return 301
    else:
        return 200

