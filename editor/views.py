from django.shortcuts import render
from django.http import JsonResponse
import os
import subprocess

# Create your views here.
def text_editor(request):

    #Unique filename for the user's code
    filename = 'temp_{}.cpp'.format(request.session.session_key)

    if request.method == 'POST':
        code = request.POST.get('code')
        # Write the code to the user's unique file
        with open(filename, 'w') as f:
            f.write(code)
        # Compile the code, capturing the error message if any
        compile_cmd = ['g++', '-Wall', '-Werror', '-o', filename[:-4], filename]
        p = subprocess.Popen(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            error = err.decode('utf-8')
            # Delete the user's unique file
            os.remove(filename)
            # Render the template with the error message
            return render(request, 'editor/text_editor.html', {'error': error, 'code': code})

        # Run the code and capture the output
        run_cmd = ['./{}'.format(filename[:-4])]
        p = subprocess.Popen(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        output = out.decode('utf-8')

        # Delete the user's unique file
        os.remove(filename)

        # Render the template with the output and error messages
        return render(request, 'editor/text_editor.html', {'output': output, 'code': code})

    return render(request, 'editor/text_editor.html')