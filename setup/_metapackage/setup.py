import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-opnsynid-subscription",
    description="Meta package for open-synergy-opnsynid-subscription Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-subscription_auto_close',
        'odoo11-addon-subscription_auto_generate_invoice',
        'odoo11-addon-subscription_date_end',
        'odoo11-addon-subscription_hierarchy',
        'odoo11-addon-subscription_multiple_approval',
        'odoo11-addon-subscription_no_auto_subscription',
        'odoo11-addon-subscription_payment_schedule',
        'odoo11-addon-subscription_payment_status',
        'odoo11-addon-subscription_person_in_charge',
        'odoo11-addon-subscription_related_attachment',
        'odoo11-addon-subscription_state_change_constrains',
        'odoo11-addon-subscription_template_product',
        'odoo11-addon-subscription_user_login',
        'odoo11-addon-subscription_workflow_activity',
        'odoo11-addon-subscription_workflow_policy',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
