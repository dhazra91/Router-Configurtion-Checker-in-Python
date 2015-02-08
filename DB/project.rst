Project Summary
===============

Goals achieved
--------------

1) Role Based privileges i.e report visibility based on organizational structure.
2) Check the existing configuration against a pre-defined configuration. This checking can be a role based checking as in if a router is part (role) of RIP scheme, its startup configuration will be different from router which is running OSPF. This role can also be on the basis of service that the router is supporting.
3) SLA can be attributed for routers if it does not comply with the expected startup configuration.
4) Graphical representation showing the non-compliant routers in red and compliant routers in green.
5) Automated emailand text message will be sent to the network admin at end of a compliance check cycle indicating compliance and non-compliance statistics.

Lessons Learned
---------------

1) Learned to use the sqlite3 module to create a database of users.
2) Learned to use networkx to build a topology showing the SLA compliant and non-compliant routers.
3) Learned to use TKinter to develop the GUI for the compliance test application.
4) Learned to use twilio module to send automated texts.


Future Scope
--------------

1) The compliance test could also be automated such that it can run periodically. Currently, it is run at the will of the network admin and the user.
2) I would love to learn python flask and genrate a web application

