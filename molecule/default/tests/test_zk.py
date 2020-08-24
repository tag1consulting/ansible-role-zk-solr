"""Zookeeper integration tests"""

def test_zk_packages(host):
    packages = ['libselinux-python']

    for p in packages:
        t = host.package(p)

        assert t.is_installed

def test_zk_user_group(host):
    g = host.group('zookeeper')

    assert g.exists

    u = host.user('zookeeper')

    assert u.exists
    assert u.group == 'zookeeper'

def test_zk_symlink(host):
    d = host.file("/opt/zookeeper")

    assert d.exists
    assert d.is_symlink
    assert d.linked_to == '/opt/zookeeper-3.6.1'

def test_zk_files(host):
    dirs = [
            '/opt/zookeeper-3.6.1',
            '/opt/zookeeper/bin',
            '/var/lib/zookeeper',
            '/var/log/zookeeper',
            '/opt/zookeeper/conf/zoo.cfg',
            '/opt/zookeeper/conf/log4j.properties',
            '/var/lib/zookeeper/myid'
           ]

    for d in dirs:
        tmp = host.file(d)

        assert tmp.exists
        assert tmp.user == 'zookeeper'
        assert tmp.group == 'zookeeper'

# def test_zk_service(host):
#     s = host.service('zookeeper')
# 
#     assert s.is_running
#     assert s.is_enabled
# 
#     c = host.run('/opt/zookeeper/bin/zkServer.sh status')
# 
#     assert c.rc == 0
