import ras_1c

plt_version = input('platform version (8.3.x.x)')
plt_arch = input('platform architecture (32 or 64)')
run_local_ras   = input('run local RAS? (1 or 0)')
if run_local_ras == 0:
    ras_hostname = input('RAS hostname:')
else:
    ras_hostname = 'localhost'
ras_port   = input('RAS port (1545):')
cluster_hostname   = input('1c cluster hostname:')
cluster_port   = input('1c cluster port (1540):')


ras_connect = ras_1c.Ras_connection(plt_version, plt_arch, ras_hostname, ras_port, cluster_hostname, cluster_port)
ras_cluster = ras_connect.get_cluster_by_hostname(cluster_hostname)
