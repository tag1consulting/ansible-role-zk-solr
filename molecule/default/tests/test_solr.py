"""Solr integration tests"""

def test_solr_packages(host):
    packages = ['lsof', 'acl', 'sudo']

    for p in packages:
        t = host.package(p)

        assert t.is_installed

def test_solr_user_group(host):
    g = host.group('solr')

    assert g.exists

    u = host.user('solr')

    assert u.exists
    assert u.group == 'solr'

def test_solr_symlink(host):
    d = host.file("/opt/solr")

    assert d.exists
    assert d.is_symlink
    assert d.linked_to == '/opt/solr-6.2.0'

def test_solr_files(host):
    dirs = [
            '/opt/solr-6.2.0',
            '/opt/solr/bin',
            '/var/solr',
            '/var/solr/data/',
            '/var/solr/logs',
            '/var/solr/data/solr.xml'
           ]

    for d in dirs:
        tmp = host.file(d)

        assert tmp.exists
        assert tmp.user == 'solr'
        assert tmp.group == 'solr'

def test_solr_service(host):
    s = host.service('solr')

    assert s.is_running
    assert s.is_enabled
