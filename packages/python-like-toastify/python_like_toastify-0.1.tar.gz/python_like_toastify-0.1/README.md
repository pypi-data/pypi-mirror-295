# Django Toast Messages

A simple and reusable Django app for displaying customizable toast messages. This library helps you easily show toast notifications for different message types like success, error, info, and warning, with options to customize timeout, background color, and position.

## Features

- Customizable toast notifications.
- Supports different message types (`success`, `error`, `info`, `warning`).
- Customizable timeout, background color, and position.
- Integrated with Django's built-in message framework.

## Installation

1. Install the package via pip:

   ```bash
   pip install django-toast-messages
    ```
   
## Usage

To display toast notifications, use the showToast() method in your template. It will automatically display any messages passed from the Django view.

Here’s an example of how to include dynamic messages in your template:

```bash
<script>
    {% if messages %}
        {% for message in messages %}
            showToast("{{ message }}", {
                type: "{{ message.tags }}", 
                timeout: 5000, // Customize timeout
                backgroundColor: '', // Optional: leave empty for default
                position: { top: '50px', bottom: '' } // Customize position
            });
        {% endfor %}
    {% endif %}
</script>

```
## Customization Options
- type: Defines the type of the toast message (e.g., success, error, info, warning).
- timeout: How long the toast should be visible (in milliseconds). Default is 3000 ms.
- backgroundColor: Optional. Customize the background color of the toast message.
- position: Customize the position with top and/or bottom values.

## Example View
    
```bash
from django.contrib import messages
from django.shortcuts import render

def some_view(request):
    messages.success(request, "Your form was successfully submitted!")
    return render(request, 'some_template.html')
   ```

## License
This project is licensed under the MIT License.