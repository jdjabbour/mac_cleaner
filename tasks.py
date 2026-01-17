from invoke import task

from src.protect.mac_malware_scan import mac_malware_scan

@task
def search_malware(ctx):
    mac_malware_scan()