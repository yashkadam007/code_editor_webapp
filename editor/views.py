from django.shortcuts import render
from django.http import JsonResponse
import os

# Create your views here.
def text_editor(request):
    filename = 'temp_{}.cpp'.format(request.session.session_key)

    if request.method == 'POST':
        code = request.POST.get('code')
        # Write the code to the user's unique file
        with open(filename, 'w') as f:
            f.write(code)

        # Compile and run the code, storing the output or error message
        compile_cmd = 'g++ -Wall -Werror -o {} {}'.format(filename[:-4], filename)
        run_cmd = './{}'.format(filename[:-4])
        output = ''
        error = ''
        if os.system(compile_cmd) == 0:
            output = os.popen(run_cmd).read()
        else:
            error = 'Compilation error'

        # Delete the user's unique file
        os.remove(filename)
        if os.path.exists(filename[:-4]):
            os.remove(filename[:-4])

        # Return the output or error message as a JSON response

        return render(request, 'editor/text_editor.html', {'output': output, 'error': error, 'code': code})
    return render(request, 'editor/text_editor.html')