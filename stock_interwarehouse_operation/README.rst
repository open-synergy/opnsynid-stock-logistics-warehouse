.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================================
Inter-Warehouse Product Movement
================================

This module adds:

1. New picking type operation: (1) Inter-Warehouse In, and (2) Inter-Warehouse Out. Both
type operations provide more control in managing movements between warehouse.
2. New routes to automate inter-warehouse movement

Installation
============

To install this module, you need to:

1.  Clone the branch 8.0 of the repository https://github.com/open-synergy/opnsynid-stock-logistics-warehouse
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list
4.  Go to menu *Setting -> Modules -> Local Modules*
5.  Search For *Inter-Warehouse Product Movement*
6.  Install the module

Configuration
=============

**Create Transit Pull Location**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Transit Pull Location** button

**Create Transit Push Location**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Transit Push Location** button

**Create Inter-Warehouse In Picking Type**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Inter-Warehouse In Picking Type** button

**Create Inter-Warehouse Out Picking Type**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Inter-Warehouse Out Picking Type** button

**Create Inter-Warehouse In Picking Type**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Inter-Warehouse In Picking Type** button

**Create Inter-Warehouse Pull Route**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Inter-Warehouse Pull Route** button

**Create Inter-Warehouse Push Route**

1. Go to menu **Warehouse -> Configuration -> Warehouse**
2. Open warehouse data
3. Go to **Technical Information**
4. Click **Create Inter-Warehouse Pull Route** button

Note:
All above configuration field can be filled manually if there are already data that match
the functionality


Usage
=====

**Create Pull Movement Manually From Destination Warehouse Into Source Warehouse**

#. Create stock picking manually. Make sure it has:
    * Destination warehouse's **Inter-Warehouse In** picking type
    * Source warehouse's **Transit Pull** location for source location
    * Any destination warehouse's internal location for destination location
#. Mark as to do
#. Odoo will create stock picking with **Inter-Warehouse Out** type that belong to source warehouse
#. Process and transfer Inter-Warehouse Out
#. Process and transfer Inter-Warehouse In


**Create Push Movement Manually From Source Warehouse Into Destination Warehouse**

#. Create stock picking manually. Make sure it has:
    * Destination warehouse's **Inter-Warehouse Out** picking type
    * Any Source warehouse's **internal location** for source location
    * Destination warehouse's **Transit Push** location for destination location
#. Mark as to do
#. Odoo will create stock picking with **Inter-Warehouse In** type that belong to destination warehouse
#. Process and transfer Inter-Warehouse Out
#. Process and transfer Inter-Warehouse In


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/opnsynid-stock-logistics-warehouse/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed
and welcomed feedback.

Credits
=======

Contributors
------------

* Michael Viriyananda <viriyananda.michael@gmail.com>
* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id.com

This module is maintained by the PT. Simetri Sinergi Indonesia.
