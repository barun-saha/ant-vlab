author__= "barun"
date__  = "$3 Sep, 2011 11:38:54 PM$"

# (Rev #32: #1)

from django.http import HttpResponse, HttpResponseRedirect
from vlabs.ant import tasks
import celery
import json


# Return current state of a task
def task_state(request, uuid):
    output = {'state': celery.result.AsyncResult(uuid).state}

    #with open('/var/vlabs/ant/celery.log', 'a') as log:
	#log.write(uuid + ': ' + str(output) + '\n')

    return HttpResponse(json.dumps(output), mimetype='application/json')


#def is_task_done(request, uuid):
#    output = {'done': celery.result.AsyncResult(uuid).ready() }
#    return HttpResponse(json.dumps(output), mimetype='application/json')


# Return result of the task if done
# Otherwise a message is sent back
def task_result(request, uuid):    
#    output = {'state': celery.result.AsyncResult(uuid).state}

#    with open('/var/vlabs/ant/celery.log', 'a') as log:
#        log.write('Result: ' + uuid + ': ' + str(output) + '\n')

    if celery.result.AsyncResult(uuid).ready():

        output = celery.result.AsyncResult(uuid).get()
        #with open('/var/vlabs/ant/celery.log', 'a') as log:
            #log.write('Output' + ': ' + str(output) + '\n')

        # Store the physical path of the trace file in seesion
        # and remove it from output        
        if 'trace_file_name' in output:
            request.session[request.session.session_key] = {'trace_file_name' : output['trace_file_name']}
            output.pop('trace_file_name')
    else:
        output = {'mesg': 'Still working ...'}        
        
    return HttpResponse(json.dumps(output), mimetype='application/json')
