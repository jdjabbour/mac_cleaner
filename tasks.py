from invoke import task

from src.protect.mac_malware_scan import mac_malware_scan
from src.performance.maintenance.flush_dns import flush_mac_dns
from src.performance.maintenance.free_purgeable_space import purge_space
from src.performance.maintenance.reindex_spotlight import reindex_spotlight
from src.cleanup.empty_all_trash_mac import empty_all_trash
from src.cleanup.clean_universal_binaries_mac import clean_binaries
from src.cleanup.clean_system_junk_mac import clean_system_junk

@task
def mw_scan(ctx):
    mac_malware_scan()

@task
def flush_dns(ctx):
    flush_mac_dns()

@task
def purge_mac(ctx):
    purge_space()


@task
def reindex(ctx):
    reindex_spotlight()


@task
def empty_trash(ctx):
    empty_all_trash()

@task
def cl_binary(ctx):
    clean_binaries()

@task
def cl_junk(ctx):
    clean_system_junk()