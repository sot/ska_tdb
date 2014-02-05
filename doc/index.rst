Ska.tdb
========
Access the Chandra Telemetry Database

The ``Ska.tdb`` package provides a convenient mechanism to retrieve all data in
the Chandra ODB Telemetry Database (TDB) tables.  The default values correspond
to the P010 definitions available in the CSV (text) dump of the TDB.  Versions
P004, P006, P007, P008, and P009 are also accessible (see `TDB version`_).

A description of the tables is availble in the `TDB table definitions`_ section.

Usage
----------

The TDB table entries can be accessed via the module-level variables ``tables``
and ``msids``.  The ``msids`` variable is the main workhorse for ``Ska.tdb``, while
the ``tables`` variable is needed for tables that do not have an MSID column.

Msids
^^^^^^

The ``msids`` variable allows access to all information related to a particular
MSID.  It behaves like a Python dict where you use the MSID name
(case-insenstive) as the key.  Once you have a particular MSID selected you can
then retrieve all table entries related to that MSID by accessing attributes
corresponding to the TDB table name.

Examples::

  >>> from Ska.tdb import msids
  >>> msids.<TAB>  # See available attributes

This returns the following, where all the TDB tables with MSID data begin with
capital "T" and columns from the ``tmsrment`` table are available as lower case
attributes::

  msids.Tcntr                        msids.calibration_type        msids.limit_switch_msid
  msids.Tlmt                         msids.counter_msid            msids.low_raw_count
  msids.Tloc                         msids.data_type               msids.msid
  msids.Tmsrment                     msids.description             msids.owner_id
  msids.Tpc                          msids.ehs_header_flag         msids.prop
  msids.Tpp                          msids.eng_unit                msids.range_msid
  msids.Tsc                          msids.es_default_set_num      msids.technical_name
  msids.Tsmpl                        msids.es_switch_msid          msids.total_length
  msids.calibration_default_set_num  msids.high_raw_count          
  msids.calibration_switch_msid      msids.limit_default_set_num 

If you examine any of those attributes for the ``msids`` variable you get the results for all MSIDS.

Now select a particular MSID and see that it has the same attributes::

  >>> tephin = msids['tephin']
  >>> tephin.<TAB>  # See available attributes
  tephin.Tcntr                        tephin.calibration_type             tephin.limit_default_set_num
  tephin.Tlmt                         tephin.counter_msid                 tephin.limit_switch_msid
  tephin.Tloc                         tephin.data_type                    tephin.low_raw_count
  tephin.Tmsrment                     tephin.description                  tephin.msid
  tephin.Tpc                          tephin.ehs_header_flag              tephin.owner_id
  tephin.Tpp                          tephin.eng_unit                     tephin.prop
  tephin.Tsc                          tephin.es_default_set_num           tephin.range_msid
  tephin.Tsmpl                        tephin.es_switch_msid               tephin.technical_name
  tephin.calibration_default_set_num  tephin.find                         tephin.total_length
  tephin.calibration_switch_msid      tephin.high_raw_count               

Finally look at the attributes::

  >>> tephin.Tmsrment  # MSID definition (description, tech name etc)
  ('TEPHIN', 'EPHIN SENSOR HOUSING TEMP', 'IUNS', 'PP', 'DEGF', 0, 255, 8, 
   'N', '0', '0', '0', 1, '0', 1, '0', 0, 'THM', 'LR/15/PA/2', 'U')
  >>> tephin.Tpp  # Calibration point pair values
  array([('TEPHIN', 1, 15, 232, -51.90456), ('TEPHIN', 1, 9, 110, 47.0923),
         ('TEPHIN', 1, 14, 223, -38.30814),
         ('TEPHIN', 1, 13, 214, -27.81212),
         ('TEPHIN', 1, 12, 203, -17.23066), ('TEPHIN', 1, 11, 190, -6.5357),
         ('TEPHIN', 1, 10, 172, 6.45808), ('TEPHIN', 1, 16, 255, -103.49045),
         ('TEPHIN', 1, 1, 0, 215.03), ('TEPHIN', 1, 7, 76, 72.95052),
         ('TEPHIN', 1, 6, 64, 84.09784), ('TEPHIN', 1, 5, 54, 94.86368),
         ('TEPHIN', 1, 4, 46, 104.89), ('TEPHIN', 1, 3, 38, 116.7678),
         ('TEPHIN', 1, 2, 28, 135.846), ('TEPHIN', 1, 8, 91, 60.77076)], 
        dtype=[('MSID', '|S14'), ('CALIBRATION_SET_NUM', '<i8'), ('SEQUENCE_NUM', '<i8'),
               ('RAW_COUNT', '<i8'), ('ENG_UNIT_VALUE', '<f8')])
  >>> tephin.Tsc  # No state codes so it returns None
  >>> tephin.technical_name
  'EPHIN SENSOR HOUSING TEMP'
  >>> tephin.data_type
  'IUNS'

Finding MSIDs
++++++++++++++

With the ``msids`` object you can search the TDB for MSIDs of interest::

  >>> msids.find('teph')

This returns a list of :class:`~Ska.tdb.tdb.MsidView` objects::

  [<MsidView msid="TEPHIN" technical_name="EPHIN SENSOR HOUSING TEMP">,
   <MsidView msid="TEPHTRP1" technical_name="HTR ENA/DIS: EIA/RCTU-EP/PSU1 PRI (CH0)">,
   <MsidView msid="TEPHTRP2" technical_name="HTR ENA/DIS: EIA/RCTU-EP/PSU1 PRI (CH1)">,
   <MsidView msid="TEPHTRR1" technical_name="HTR ENA/DIS: EIA/RCTU-EP/PSU1 RDNT (CH0)">,
   <MsidView msid="TEPHTRR2" technical_name="HTR ENA/DIS: EIA/RCTU-EP/PSU1 RDNT (CH1)">]

If required you can dig deeper, for instance::

  >>> tephs = msids.find('teph')
  >>> for x in tephs:
  ...     print(x.msid, x.description, x.data_type)
  ('TEPHIN', 'LR/15/PA/2', 'IUNS')
  ('TEPHTRP1', 'EP/3/SD/0 ISATS MOM BEIA0W01 BIT 3 EIA/RCTU-EP PRI HTR ON/OFF (CH0)', 'IDIS')
  ('TEPHTRP2', 'EP/3/SD/1 ISATS MOM BEIA1W01 BIT 3 EIA/RCTU-EP PRI HTR ON/OFF (CH1)', 'IDIS')
  ('TEPHTRR1', 'EP/3/SD/0 ISATS MOM BEIA0W09 BIT 3 EIA/RCTU-EP RDNT HTR ON/OFF (CH0)', 'IDIS')
  ('TEPHTRR2', 'EP/3/SD/1 ISATS MOM BEIA1W09 BIT 3 EIA/RCTU-EP RDNT HTR ON/OFF (CH1)', 'IDIS')

Tables
^^^^^^^^

The ``tables`` variable allows direct access to TDB tables.  This variable is a
special dict object that returns a ``TableView`` object when you ask for a TDB
table such as ``tmsrment`` (MSID descriptions) or ``tsc`` (MSID state codes).

After you import the ``tables`` variable you can ask for the names of all
available tables::

  from Ska.tdb import tables
  tables.keys()  # show all available tables

You then select a table with the table name (which must be lower case)::

  >>> tmsrment = tables['tmsrment']

With this table selected you can show the table, show all columns for that
table, or get the values for a particular column::

  >>> tmsrment  # show the table
    ... <SNIP> ...
  >>> tmsrment.colnames  # column names for this table
  ('MSID', 'TECHNICAL_NAME', 'DATA_TYPE', 'CALIBRATION_TYPE', 'ENG_UNIT', 'LOW_RAW_COUNT',
  'HIGH_RAW_COUNT', 'TOTAL_LENGTH', 'PROP', 'COUNTER_MSID', 'RANGE_MSID', 'CALIBRATION_SWITCH_MSID',
  'CALIBRATION_DEFAULT_SET_NUM', 'LIMIT_SWITCH_MSID', 'LIMIT_DEFAULT_SET_NUM', 'ES_SWITCH_MSID',
  'ES_DEFAULT_SET_NUM', 'OWNER_ID', 'DESCRIPTION', 'EHS_HEADER_FLAG')
  >>> tmsrment['technical_name']
  array(['OFFLINE SCIENCE DATA FOR ACIS 1 OF 2',
         'OFFLINE SCIENCE DATA FOR ACIS ADDITIONAL', 'CAMERA BODY TEMP. A',
         ..., 'RCS-2 thruster valve 01 temperature (OBC reading)',
         'RCS-2 thruster valve 02 temperature (OBC reading)',
         'ACIS High Radiation Flag'], 
        dtype='|S59')

For tables that have an MSID column you can filter on the MSID to see only
entries for that MSID.  The MSID names are case-insensitive.

  >>> tmsrment['tephin']  # only TEPHIN entries
  ('TEPHIN', 'EPHIN SENSOR HOUSING TEMP', 'IUNS', 'PP', 'DEGF', 0, 255, 8, 'N',
  '0', '0', '0', 1, '0', 1, '0', 0, 'THM', 'LR/15/PA/2', 'U')
  >>> tables['tsc']['aoattqt4']  # State codes for AOATTQT4
  array([], dtype=[('MSID', '|S15'), ('CALIBRATION_SET_NUM', '<i8'), ('SEQUENCE_NUM', '<i8'),
  ('LOW_RAW_COUNT', '<i8'), ('HIGH_RAW_COUNT', '<i8'), ('STATE_CODE', '|S4')])
  >>> tables['tpp']['TEPHIN']  # Point pair for TEPHIN
  array([('TEPHIN', 1, 15, 232, -51.90456), ('TEPHIN', 1, 9, 110, 47.0923),
         ('TEPHIN', 1, 14, 223, -38.30814),
         ('TEPHIN', 1, 13, 214, -27.81212),
         ('TEPHIN', 1, 12, 203, -17.23066), ('TEPHIN', 1, 11, 190, -6.5357),
         ('TEPHIN', 1, 10, 172, 6.45808), ('TEPHIN', 1, 16, 255, -103.49045),
         ('TEPHIN', 1, 1, 0, 215.03), ('TEPHIN', 1, 7, 76, 72.95052),
         ('TEPHIN', 1, 6, 64, 84.09784), ('TEPHIN', 1, 5, 54, 94.86368),
         ('TEPHIN', 1, 4, 46, 104.89), ('TEPHIN', 1, 3, 38, 116.7678),
         ('TEPHIN', 1, 2, 28, 135.846), ('TEPHIN', 1, 8, 91, 60.77076)], 
        dtype=[('MSID', '|S14'), ('CALIBRATION_SET_NUM', '<i8'), ('SEQUENCE_NUM', '<i8'),
               ('RAW_COUNT', '<i8'), ('ENG_UNIT_VALUE', '<f8')])

TDB version
^^^^^^^^^^^

P010 is the default version of the TDB that is accessed.  To change this, specify
the new version as an integer, e.g. ``8`` for version P008.  In this example we
roll back time to P008 when the TEPHIN database limits were much lower::

  >>> msids['tephin'].Tlmt
  ('TEPHIN', 1, 10.0, 150.0, 5.0, 999.0, 0, 5, 'A')

  >>> import Ska.tdb
  >>> Ska.tdb.set_tdb_version(8)

  >>> msids['tephin'].Tlmt
  ('TEPHIN', 1, 10.0, 81.0, 5.0, 86.0, 0, 5, 'A')

API Documentation
------------------
.. toctree::
   :maxdepth: 2

   Ska.tdb_api

TDB table definitions
-----------------------

tcntr
^^^^^^^^^^^^^^^^^^^^^^^^^

================ ==========
  Column         Type 
================ ==========
MSID             string(8)
STREAM_NUMBER    int  
INIT_VALUE       int  
END_VALUE        int  
WRAP_AROUND_FLAG string(1)
DIR              string(1)
DELTA            int  
COUNTER_TYPE     string(3)
================ ==========

tes
^^^^^^^^^^^^^^^^^^^^^^^^^

================ ==========
  Column         Type 
================ ==========
MSID             string(15)
ES_SET_NUM       int  
EXPECTED_STATE   string(4)
TOLER            int  
EM_ALL_SAMP_FLAG string(1)
================ ==========

tlmt
^^^^^^^^^^^^^^^^^^^^^^^^^

================ ==========
  Column         Type 
================ ==========
MSID             string(14)
LIMIT_SET_NUM    int  
CAUTION_LOW      float
CAUTION_HIGH     float
WARNING_LOW      float
WARNING_HIGH     float
DELTA            int  
TOLER            int  
EM_ALL_SAMP_FLAG string(1)
================ ==========

tloc
^^^^^^^^^^^^^^^^^^^^^^^^^

================= ==========
  Column          Type 
================= ==========
MSID              string(15)
STREAM_NUMBER     int  
SYLLABLE_NUMBER   int  
START_MINOR_FRAME int  
START_WORD        int  
START_BIT         int  
LENGTH            int  
================= ==========

tmsrment
^^^^^^^^^^^^^^^^^^^^^^^^^

=========================== ==========
  Column                    Type 
=========================== ==========
MSID                        string(15)
TECHNICAL_NAME              string(59)
DATA_TYPE                   string(4)
CALIBRATION_TYPE            string(2)
ENG_UNIT                    string(7)
LOW_RAW_COUNT               int  
HIGH_RAW_COUNT              int  
TOTAL_LENGTH                int  
PROP                        string(1)
COUNTER_MSID                string(8)
RANGE_MSID                  string(8)
CALIBRATION_SWITCH_MSID     string(8)
CALIBRATION_DEFAULT_SET_NUM int  
LIMIT_SWITCH_MSID           string(8)
LIMIT_DEFAULT_SET_NUM       int  
ES_SWITCH_MSID              string(7)
ES_DEFAULT_SET_NUM          int  
OWNER_ID                    string(4)
DESCRIPTION                 string(240)
EHS_HEADER_FLAG             string(1)
=========================== ==========

towner
^^^^^^^^^^^^^^^^^^^^^^^^^

=========== ==========
  Column    Type 
=========== ==========
OWNER_ID    string(4)
DESCRIPTION string(53)
=========== ==========

tpc
^^^^^^^^^^^^^^^^^^^^^^^^^

=================== ==========
  Column            Type 
=================== ==========
MSID                string(9)
CALIBRATION_SET_NUM int  
ENG_UNIT_LOW        float
ENG_UNIT_HIGH       float
DEG                 int  
COEF0               float
COEF1               float
COEF2               float
COEF3               float
COEF4               float
COEF5               float
COEF6               float
COEF7               float
COEF8               float
COEF9               float
=================== ==========

tpp
^^^^^^^^^^^^^^^^^^^^^^^^^

=================== ==========
  Column            Type 
=================== ==========
MSID                string(14)
CALIBRATION_SET_NUM int  
SEQUENCE_NUM        int  
RAW_COUNT           int  
ENG_UNIT_VALUE      float
=================== ==========

tsc
^^^^^^^^^^^^^^^^^^^^^^^^^

=================== ==========
  Column            Type 
=================== ==========
MSID                string(15)
CALIBRATION_SET_NUM int  
SEQUENCE_NUM        int  
LOW_RAW_COUNT       int  
HIGH_RAW_COUNT      int  
STATE_CODE          string(4)
=================== ==========

tsmpl
^^^^^^^^^^^^^^^^^^^^^^^^^

==================== ==========
  Column             Type 
==================== ==========
MSID                 string(15)
STREAM_NUMBER        int  
PAR_COMP             string(2)
SAMPLE_PER_GROUP     int  
GROUP_SAMPLE_OFSET   int  
SAMPLE_COMP          string(1)
SAMPLE_RATE          int  
OFSET                int  
START_COUNTER_VALUE  int  
COUNTER_OFSET        int  
LOW_RANGE            int  
HIGH_RANGE           int  
STATE_CODE           string(4)
CONTEXT_PACKET_ID    int  
CONTEXT_LVT_LOCATION int  
==================== ==========

tstream
^^^^^^^^^^^^^^^^^^^^^^^^^

================== ==========
  Column           Type 
================== ==========
STREAM_NUMBER      int  
STREAM_TYPE        string(1)
STREAM_ID          string(4)
STREAM_FORMAT_ID   string(3)
PROTOCOL           int  
STREAM_PRIORITY    int  
STREAM_PROP        string(1)
STREAM_OWNER_ID    string(4)
STREAM_DESCRIPTION string(38)
================== ==========

ttdm
^^^^^^^^^^^^^^^^^^^^^^^^^

================= ==========
  Column          Type 
================= ==========
TDM_ID            string(4)
FORMAT_ID_MSID    string(8)
TIME_MSID         string(1)
SYNC_PATTERN      string(6)
SYNC_PATTERN_MSID string(7)
SYNC_LENGTH       int  
================= ==========

ttdm_fmt
^^^^^^^^^^^^^^^^^^^^^^^^^

============================ ==========
  Column                     Type 
============================ ==========
TDM_ID                       string(4)
TDM_FORMAT_ID                string(3)
FORMAT                       int  
BITS_PER_WORD                int  
WORDS_PER_MINOR_FRAME        int  
MINOR_FRAMES_PER_MAJOR_FRAME int  
DATA_CYCLE                   int  
MAJOR_FRAME_PERIOD           float
ENCAP_STREAM_NUMBER          int  
ENCAP_BOUNDARY               string(1)
ENCAP_FRAME_PER_PACKET       int  
============================ ==========

