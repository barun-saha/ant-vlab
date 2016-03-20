# (Rev #32: #1)
import django_rq
from django.conf import settings
from django.http import HttpResponse
import time

import subprocess as sp
import os
import re
import json
import globals

#import sys
#sys.stdout = sys.stderr


# 23 Oct 2013
from django.contrib.sessions.backends.db import SessionStore


def ns2run(code, session_key):
    #code = request.POST.get('ns2code')
    #print 'Session key:', session_key
    #print 'ns2run'
    script_file_name = 'script_' + session_key
    script_file_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key + '/' + script_file_name
    user_dir_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key

#    with open(LOG_FILE, 'a') as log_file:
#	log_file.write('[ns2]', script_file_name)

    #print script_file_path

    is_error = False
    error_mesg = ''
    script_file = None

    # Store the user program in a temporary file
    try:
        script_file = open(script_file_path, 'w')
        script_file.write(code)
    except IOError, ioe:
        is_error = True
        error_mesg = str(ioe)
        try:
            os.mkdir(user_dir_path)
            script_file = open(script_file_path, 'w')
            script_file.write(code)
            is_error = False
        except OSError, ose:
            is_error = True
            error_mesg = str(ose)
    except Exception, e:
        is_error = True
        error_mesg = str(e)
    finally:
        if script_file:
            script_file.close()
        if is_error:
            return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    is_error = False

    # Substitute certain strings in the user script
    # Any file set to create within the program will be created at /var/vlabs_demo/ant
    changed_contents = ''
    try:
        script_file = open(script_file_path, 'r')
        changed_contents = re.sub(r'(\[\s*\bopen\s+)\b(.*?)\s+(w\s*\])',
                                r'\1 ' + user_dir_path + r'/\2 \3',
                                script_file.read()
        )
        script_file.close()

        # Disable any exec statement present in the script
        changed_contents = re.sub(r'(\bexec\b)', r'#\1', changed_contents)

        # (Rev #35: #1)
        # Replace PED_A (or PED_B) with globals.WIMAX_REF_PATH/PED_A (or
        # globals.WIMAX_REF_PATH/PED_B)
        changed_contents = re.sub( r'(\s*ITU_PDP\s*)(.*PED_A).*',
                                    r'\1' + '"' + globals.WIMAX_REF_PATH + '/PED_A"',
                                    changed_contents )
        changed_contents = re.sub( r'(\s*ITU_PDP\s*)(.*PED_B).*',
                                    r'\1' + '"' + globals.WIMAX_REF_PATH + '/PED_B"',
                                    changed_contents )

        script_file = open(script_file_path, 'w')
        script_file.write(changed_contents)
        script_file.close()
        #print changed_contents
        #return HttpResponse(changed_contents)
    except IOError, ioe:
        is_error = True
        error_mesg = str(ioe)
        return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    # Flags for files
    trace_file_exists = False
    nam_trace_file_exists = False

    # Find the name of the trace file, if any
    trace_file_var = None
    trace_file_name = None
    trace_file_path = None
    mobj = re.search(r'\s*[$]{1}\w+\s+trace-all\s+[$]{1}([\w-]+)', changed_contents)
    if mobj:
        trace_file_var = mobj.group(1)
        declaration_pattern = r'set\s+%s\s+\[\s*open\s+([\w./-]+)\s+w\s*\]' % (trace_file_var,)
        #print declaration_pattern
        mobj = None
        #print changed_contents
        mobj = re.search(declaration_pattern, changed_contents)
        if mobj:
            trace_file_name = mobj.group(1)
            trace_file_exists = True
            #trace_file_path = globals.NS2_SCRIPT_STORAGE_PATH + '/' + session_key + '/' + trace_file_name

    #print 'Trace file: ', trace_file_name
    # Generate the argument list
    args = (globals.NS2_PATH, script_file_path,)
    #print args

    # Spawn the sub process
    process = sp.Popen(args, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    result, error =  process.communicate()
    #print process.returncode

    if process.returncode != 0:
            mesg = 'An error occured while executing your script!'
            trace_file_exists = False
    else:
            mesg = 'Successful!'

    mesg += '\n' + result
    if error:
        mesg += '\n' + error

    mesg = re.sub(session_key, 'XXX', mesg)     # Hide the session ID
    mesg = re.sub(globals.NS2_SCRIPT_STORAGE_PATH, r'[base]', mesg)         # Hide the server storage path
    #print mesg
    output = {'mesg': mesg,}

    #print 'Trace file:', trace_file_name

    if trace_file_exists:
        # *** Store trace file name for the current user session ***

        # ??? Trace file name ???
        #request.session[request.session.session_key] = {'trace_file_name' : trace_file_name}
	# 22 Oct 2013
	# Save the trace file name in the user session
	s = SessionStore(session_key)
	s[session_key] = {'trace_file_name' : trace_file_name}
	s.save()
        #

        #print request.session.get(request.session.session_key)
        output['trace_file_name'] = trace_file_name

        # Convert physical path of trace file to URL
        output['trace'] = trace_file_name.replace(r'/var/', settings.MEDIA_URL)
        #print trace_file_name
        # Return the contrnts of the trace file
        try:
            tr_file = open(trace_file_name, 'r')
            output['trace'] = tr_file.readlines()
        except IOError, ioe:
            output['error'] = str(ioe)
        finally:
            if tr_file:
                tr_file.close()
    else:
        output['trace'] = ''

    #print 'Output:', output
    return output



def ns3run(code, session_key):
    #code = request.POST.get('ns3code')
    #print request.session.session_key
    #return HttpResponse(json.dumps({'mesg': 'Working'}))

    script_file_name = 'script_' + session_key  # Without .cc extension
    script_file_path_cc =  '/'.join([globals.NS3_SCRIPT_STORAGE_PATH, script_file_name,])  + '.cc'
    user_dir_path = globals.NS3_SCRIPT_STORAGE_PATH

    is_error = False
    error_mesg = ''
    script_file = None

    # Store the user program in a temporary file
    try:
        script_file = open(script_file_path_cc, 'w')
        script_file.write(code)
    except IOError, ioe:
        is_error = True
        error_mesg = str(ioe)
        try:
            os.mkdir(user_dir_path)
            script_file = open(script_file_path_cc, 'w')
            script_file.write(code)
            is_error = False
        except OSError, ose:
            is_error = True
            error_mesg = str(ose)
    except Exception, e:
        is_error = True
        error_mesg = str(e)
    finally:
        if script_file:
            script_file.close()
        if is_error:
            return HttpResponse('<p class="error">Error: ' + error_mesg + '</p>')

    is_error = False


    os.chdir(globals.NS3_INSTALL_PATH)
    args = ( 'python', 'waf', '--run', '/'.join( (globals.NS3_SYM_LINK, script_file_name,) ) )
    #print args

    # Spawn the sub process
    process = sp.Popen(args, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
    result, error =  process.communicate()
    #print process.returncode

    # Remove directory info from outputs

    #print 'Result:', result
    #print 'Error:', error
    #result = result.replace('Entering directory', '').replace('Leaving directory', '').replace('cxx: ns3', '').replace('cxx_link:', '');
    #error = error.replace('Entering directory', '').replace('Leaving directory', '').replace('cxx: ns3', '').replace('cxx_link:', '');
    if process.returncode != 0:
        mesg = 'An error occured while executing your script!\n\n'
    else:
        mesg = ''

    mesg += result
    if error:
        mesg += '\n' + error

    filtered_msg = ''
    # Credits: http://bytes.com/topic/python/answers/585607-more-efficient-fnmatch-fnmatch-multiple-patterns#post2297793
    patterns = [r'^Waf', r'\'build\' finished', r'build\/debug\/ns3']
    pats = re.compile('|'.join(patterns))

    for line in mesg.splitlines():
        if not pats.search(line):
            filtered_msg = os.linesep.join([filtered_msg, line,])

    #mesg = re.sub(request.session.session_key, 'XXX', mesg)     # Hide the session ID
    #mesg = re.sub(globals.NS2_SCRIPT_STORAGE_PATH, r'[base]', mesg)         # Hide the server storage path
    #print mesg
    #print filtered_msg
    output = {'mesg': filtered_msg,}

    return output


def job_result(request, uuid):
    job = django_rq.get_queue(name=settings.REDIS_QNAME).fetch_job(uuid)
    output = {
        'status': job.status,
        'result': job.result,
    }

    return HttpResponse(json.dumps(output), content_type='application/json')
