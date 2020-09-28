# Zabbix-template-for-Apache-druid-

##################################################################################
#                A monitoring solution for Apache Druid based on zabbix          #
#    Option:  1.Get failed task and which datasources it belongs to in realtime  #
#             2.Get health status of all conponents                              #
#             3.Get number of running&pending tasks                              #
#             4.Confirm whether each component is available                      #
##################################################################################

Instructions
import templates first
Put druid.py in folder zabbix_agent/share/zabbix/externalscripts/ 
Put druid.conf in folder zabbix_agent/etc/zabbix_agent.conf.d/
mkdir /tmp/druidmonitor
chmod 777 /tmp/druidmonitor
