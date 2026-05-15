import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-open-synergy-opnsynid-stock-logistics-warehouse",
    description="Meta package for open-synergy-opnsynid-stock-logistics-warehouse Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-stock_inventory_by_diff_before_validate',
        'odoo11-addon-stock_inventory_by_product_set',
        'odoo11-addon-stock_inventory_movement_before_validate',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)
