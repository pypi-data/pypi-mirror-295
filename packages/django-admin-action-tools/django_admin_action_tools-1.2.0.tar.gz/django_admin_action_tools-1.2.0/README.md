# Django Admin Confirm

[![PyPI](https://img.shields.io/pypi/v/django-admin-action-tools?color=blue)](https://pypi.org/project/django-admin-action-tools/)
![Tests Status](https://github.com/SpikeeLabs/django-admin-action-tools/actions/workflows/.github/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/SpikeeLabs/django-admin-action-tools/branch/main/graph/badge.svg?token=NK5V6YMWW0)](https://codecov.io/gh/SpikeeLabs/django-admin-action-tools)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-admin-action-tools)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-admin-action-tools)
![PyPI - License](https://img.shields.io/pypi/l/django_admin_action_tools)

---
## Features
- [x] AdminConfirmMixin
    Based on [django-admin-confirm](https://github.com/TrangPham/django-admin-confirm) with support for [django-object-actions](https://github.com/crccheck/django-object-actions)
    AdminConfirmMixin is a mixin for ModelAdmin to add confirmations to change, add and actions.
- [x] AdminFormMixin
    AdminFormMixin is a mixin for ModelAdmin to add a form to configure your actions.

- [x] Ability to Confirm an action form with a preview of the objects and form data

- [x] Add support to chain form

---
## ScreenShot
<details>
  <summary><b>Confirm ScreenShot</b></summary>

![Screenshot of Change Confirmation Page](https://raw.githubusercontent.com/SpikeeLabs/django-admin-action-tools/alpha/docs/images/screenshot_confirm_change.png)

![Screenshot of Add Confirmation Page](https://raw.githubusercontent.com/SpikeeLabs/django-admin-action-tools/alpha/docs/images/screenshot_confirm_add.png)

![Screenshot of Action Confirmation Page](https://raw.githubusercontent.com/SpikeeLabs/django-admin-action-tools/alpha/docs/images/screenshot_confirm_action.png)

</details>

<details>
  <summary><b>Form ScreenShot</b></summary>

![Screenshot of The Action Form](https://raw.githubusercontent.com/SpikeeLabs/django-admin-action-tools/alpha/docs/images/screenshot_action_form.png)


</details>


---
## Installation

Install django-admin-action-tools by running:

    poetry add django-admin-action-tools

Add `admin_action_tools` to `INSTALLED_APPS` in your project settings before `django.contrib.admin`:

    INSTALLED_APPS = [
        ...
        'admin_action_tools',

        'django.contrib.admin',

        ...
        'widget_tweaks'
        ...
    ]

To use `ActionFormMixin` you also need to add `widget_tweaks` to the `INSTALLED_APPS`

Note that this project follows the template override rules of Django.
To override a template, your app should be listed before `admin_confirm`, `admin_form` in INSTALLED_APPS.


## Configuration Options

**Environment Variables**:

Caching is used to cache files for confirmation. When change/add is submitted on the ModelAdmin, if confirmation is required, files will be cached until all validations pass and confirmation is received.

- `ADMIN_CONFIRM_CACHE_TIMEOUT` _default: 1000_
- `ADMIN_CONFIRM_CACHE_KEY_PREFIX` _default: admin_confirm\_\_file_cache_

**Attributes:**

- `confirm_change` _Optional[bool]_ - decides if changes should trigger confirmation
- `confirm_add` _Optional[bool]_ - decides if additions should trigger confirmation
- `confirmation_fields` _Optional[Array[string]]_ - sets which fields should trigger confirmation for add/change. For adding new instances, the field would only trigger a confirmation if it's set to a value that's not its default.
- `change_confirmation_template` _Optional[string]_ - path to custom html template to use for change/add
- `action_confirmation_template` _Optional[string]_ - path to custom html template to use for actions

Note that setting `confirmation_fields` without setting `confirm_change` or `confirm_add` would not trigger confirmation for change/add. Confirmations for actions does not use the `confirmation_fields` option.

**Method Overrides:**
If you want even more control over the confirmation, these methods can be overridden:

- `get_confirmation_fields(self, request: HttpRequest, obj: Optional[Object]) -> List[str]`
- `render_change_confirmation(self, request: HttpRequest, context: dict) -> TemplateResponse`
- `render_action_confirmation(self, request: HttpRequest, context: dict) -> TemplateResponse`

## Usage

### AdminConfirmMixin
It can be configured to add a confirmation page on ModelAdmin upon:

- saving changes
- adding new instances
- performing actions

**Confirm Change:**

```py
    from admin_confirm import AdminConfirmMixin

    class MyModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_change = True
        confirmation_fields = ['field1', 'field2']
```

This would confirm changes on changes that include modifications on`field1` and/or `field2`.

**Confirm Add:**

```py
    from admin_confirm import AdminConfirmMixin

    class MyModelAdmin(AdminConfirmMixin, ModelAdmin):
        confirm_add = True
        confirmation_fields = ['field1', 'field2']
```

This would confirm add on adds that set `field1` and/or `field2` to a non default value.

Note: `confirmation_fields` apply to both add/change confirmations.

**Confirm Action:**

```py
    from admin_confirm import AdminConfirmMixin

    class MyModelAdmin(AdminConfirmMixin, ModelAdmin):
        actions = ["action1", "action2"]

        def action1(modeladmin, request, queryset):
            # Do something with the queryset

        @confirm_action()
        def action2(modeladmin, request, queryset):
            # Do something with the queryset

        action2.allowed_permissions = ('change',)
```

This would confirm `action2` but not `action1`.

Action confirmation will respect `allowed_permissions` and the `has_xxx_permission` methods.

> Note: AdminConfirmMixin does not confirm any changes on inlines

**Confirm Object Action:**

```py
    from admin_confirm import AdminConfirmMixin
    from django_object_actions import DjangoObjectActions

    class MyModelAdmin(AdminConfirmMixin, DjangoObjectActions, ModelAdmin):
        change_actions = ["action1"]

        @confirm_action()
        def action1(self, request, object):
            # Do something with the object
```


### AdminFormMixin
**Action Form**

```py
    from admin_confirm import ActionFormMixin, add_form_to_action
    from myapp.form import NoteActionForm
    from django_object_actions import DjangoObjectActions

    class MyModelAdmin(ActionFormMixin, DjangoObjectActions, ModelAdmin):
        change_actions = ["object_action"]

        @add_form_to_action(NoteActionForm)
        def action1(modeladmin, request, queryset, form=None):
            # Do something with the queryset

        @add_form_to_action(NoteActionForm)
        def object_action(modeladmin, request, object, form=None):
            # Do something with the object
```

**Chaining tools**

```py
    from admin_confirm import AdminConfirmMixin, ActionFormMixin, confirm_action, add_form_to_action
    from django_object_actions import DjangoObjectActions
    from myapp.form import NoteActionForm

    class MyModelAdmin(AdminConfirmMixin, ActionFormMixin, DjangoObjectActions, ModelAdmin):
        change_actions = ["action1"]

        @add_form_to_action(NoteActionForm)
        @confirm_action()
        def action1(self, request, object, form=None):
            # Do something with the object
```
This will chain form and confirmation.
The confirmation page will have the actions & form values displayed.
If you only want the action (same as confirm only), you can pass the following argument

```py
    from admin_confirm import AdminConfirmMixin, ActionFormMixin, confirm_action, add_form_to_action
    from django_object_actions import DjangoObjectActions
    from myapp.form import NoteActionForm

    class MyModelAdmin(AdminConfirmMixin, ActionFormMixin, DjangoObjectActions, ModelAdmin):
        change_actions = ["action1"]

        @add_form_to_action(NoteActionForm)
        @confirm_action(display_form=False)
        def action1(self, request, object, form=None):
            # Do something with the object and form
```

```py
    from admin_confirm import AdminConfirmMixin, ActionFormMixin, confirm_action, add_form_to_action
    from django_object_actions import DjangoObjectActions
    from myapp.form import NoteActionForm, SecondForm

    class MyModelAdmin(AdminConfirmMixin, ActionFormMixin, DjangoObjectActions, ModelAdmin):
        change_actions = ["action1"]

        @add_form_to_action(NoteActionForm)
        @add_form_to_action(SecondForm)
        @confirm_action()
        def action1(self, request, object, forms=None):
            # Do something with the object and forms
```
This will chain 2 forms and confirmation.
The confirmation page will have the actions & form values displayed.

if you want to not display the impacted objects, you can use

```py
    from admin_confirm import AdminConfirmMixin, ActionFormMixin, confirm_action, add_form_to_action
    from django_object_actions import DjangoObjectActions
    from myapp.form import NoteActionForm, SecondForm

    class MyModelAdmin(AdminConfirmMixin, ActionFormMixin, DjangoObjectActions, ModelAdmin):
        change_actions = ["action1"]

        @add_form_to_action(NoteActionForm, display_queryset=False)
        @add_form_to_action(SecondForm, display_queryset=False)
        @confirm_action(display_queryset=False)
        def action1(self, request, object, forms=None):
            # Do something with the object and forms
```


## Development
Check out our [development process](docs/development_process.md) if you're interested.
