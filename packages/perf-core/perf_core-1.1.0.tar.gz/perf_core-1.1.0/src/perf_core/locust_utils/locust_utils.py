from locust.exception import RescheduleTask

def validate_response_code(response, timeout=2):
    if response.status_code == 200 or response.status_code == 201:
        if response.elapsed.total_seconds() > timeout:
            response.failure("Request took more than {} seconds".format(timeout))
            raise RescheduleTask()
        else:
            response.success()
    elif str(response.status_code).startswith('4'):
        response.failure("Client side error code {}".format(response.status_code))
        raise RescheduleTask()
    elif str(response.status_code).startswith('5'):
        response.failure("Server side error code {}".format(response.status_code))

