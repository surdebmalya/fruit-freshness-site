def errors(code):
    if code==401:
        msg = 'Unauthorized Resuest'
    elif code==404:
        msg = 'Please Select A File !!!'
    elif code==500:
        msg = 'Something Went Wrong... Internal Server Error'
    return code, msg