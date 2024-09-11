
def create_user_response(result):
    response = {}
    r = result.json()
    if result.status_code == 200:
        response['status'] = 0
        if r is not None:
            response['response'] = r['response']
        response['error'] = ''
    else:
        response['status'] = -1
        response['error'] = r['detail']

    return response
