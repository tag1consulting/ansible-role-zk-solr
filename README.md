Ansible Role: Zookeeper-Solr
=========

Installs and deploys a Zookeeper managed Solr cluster.

Tested Platforms and [zookeeper]/[solr] versions

| Platform | 3.6.1 / 6.2.0 |
| :------- | :-----------: |
| centos/7 | &#x2611;	   |


Requirements
------------

Recommended to run molecule in virtualenv.

Create a virtualenv with:

	`virtualenv --python=python3 <venv_name>`

> Note: Recommended to create virtualenv outside repos root, eg. `~/.venvs/` Otherwise, linter will check virtualenv files and throw misleading errors

Once venv is activated, install requirements with:

	`pip install -r requirements.txt`

Role can then be tested with `molecule converge`

Role Variables
--------------

### Zookeeper Variables

Zookeeper version to install:

	zk_version: 3.6.1

Path tar will be downloaded to

	zk_tar_dir: /opt/src

Zookeeper install dir:

	zk_dir: "/opt/zookeeper-{{ zk_version }}"

Zookeeper home:

	zk_data_dir: /var/lib/zookeeper

Zookeeper log path:

	zk_log_dir: /var/log/zookeeper

Mirrors role will attempt to download zookeeper from

	zk_mirrors:
	  - "https://apache.osuosl.org/zookeeper/"
	  - "https://archive.apache.org/dist/zookeeper/"

Zookeeper tar checksum, algorithm, and remote path dynamically configured by default:

	zk_checksum: ""
	zk_checksum_algo: ""
	zk_remote_path: ""

User that runs zookeeper and owns corresponding files and directories:

	zk_user: zookeeper

Starts and/or restarts zookeeper service when true. Just installs zookeeper when false:

	zk_deploy: true

Controls zookeeper dynamic config overwrite:

	zk_reconfigure: false

Dictionary of key=>value pairs that populates `"{{ zk_dir }}/conf/zoo.cfg"`:

	zk_conf_params:
	  tickTime: 2000
	  initLimit: 10
	  syncLimit: 5
	  dataDir: "{{ zk_data_dir }}"
	  snapCount: 10000
	  leaderServes: yes
	  autopurge.snapRetainCount: 3
	  autopurge.purgeInterval: 0
	  4lw.commands.whitelist: "stat, ruok, conf, isro, wchc, mntr"
	  reconfigEnabled: true
	  dynamicConfigFile: "{{ zk_dir }}/conf/zoo.cfg.dynamic"

Dictionary of key=>value pairs that populate zookeeper systemd unit:

	zk_systemd_params:
	  unit:
		 Description: "Zookeeper"
		 After: network.target
		 Wants: network.target
	  service:
		 Type: simple
		 User: "{{ zk_user }}"
		 Group: "{{ zk_user }}"
		 ExecStart: "/opt/zookeeper/bin/zkServer.sh start-foreground"
		 Restart: always
		 RestartSec: 3
		 TimeoutSec: 300
	  install:
		 WantedBy: multi-user.target

Dictionary of key=>value pairs that populate log4j config:

	zk_log_params:
	  zk:
		 root.logger: "INFO,CONSOLE,ROLLINGFILE"
		 console.threshold: "INFO"
		 log.dir: "/var/log/zookeeper"
		 log.file: "zookeeper.log"
		 log.threshold: "INFO"
		 log.maxfilesize: "256MB"
		 log.maxbackupindex: "20"
	  log4j:
		 rootLogger: "${zookeeper.root.logger}"
		 appender.CONSOLE: "org.apache.log4j.ConsoleAppender"
		 appender.CONSOLE.Threshold: "${zookeeper.console.threshold}"
		 appender.CONSOLE.layout: "org.apache.log4j.PatternLayout"
		 appender.CONSOLE.layout.ConversionPattern: "%d{ISO8601} [myid:%X{myid}] - %-5p [%t:%C{1}@%L] - %m%n"
		 appender.ROLLINGFILE: "org.apache.log4j.RollingFileAppender"
		 appender.ROLLINGFILE.Threshold: "${zookeeper.log.threshold}"
		 appender.ROLLINGFILE.File: "${zookeeper.log.dir}/${zookeeper.log.file}"
		 appender.ROLLINGFILE.MaxFileSize: "${zookeeper.log.maxfilesize}"
		 appender.ROLLINGFILE.MaxBackupIndex: "${zookeeper.log.maxbackupindex}"
		 appender.ROLLINGFILE.layout: "org.apache.log4j.PatternLayout"
		 appender.ROLLINGFILE.layout.ConversionPattern: "%d{ISO8601} [myid:%X{myid}] - %-5p [%t:%C{1}@%L] - %m%n"
		 appender.TRACEFILE: "org.apache.log4j.FileAppender"
		 appender.TRACEFILE.Threshold: "TRACE"
		 appender.TRACEFILE.File: "${zookeeper.tracelog.dir}/${zookeeper.tracelog.file}"
		 appender.TRACEFILE.layout: "org.apache.log4j.PatternLayout"
		 appender.TRACEFILE.layout.ConversionPattern: "%d{ISO8601} [myid:%X{myid}] - %-5p [%t:%C{1}@%L][%x] - %m%n"

Array of dictionaries of zookeeper hosts in cluster with connection information. Defaults empty:

	zk_hosts:
		- host: "zk-solr1"
			addr: "10.0.1.111"
			id: 1
			leader_port: 2888
			election_port: 3888
			client_port: 2181
		- host: "zk-solr2"
			addr: "10.0.1.112"
			id: 2
			leader_port: 2888
			election_port: 3888
			client_port: 2181
		- host: "zk-solr3"
			addr: "10.0.1.113"
			id: 3
			leader_port: 2888
			election_port: 3888
			client_port: 2181

  
### Solr Variables

Solr version to install:

	solr_version: "6.2.0"

Path tar will be downloaded to:

	solr_tar_dir: /opt/src

Solr install dir:

	solr_dir: "/opt/solr-{{ solr_version }}"

Solr home:

	solr_data_dir: /var/solr

Mirrors role will attempt to download solr from:

	solr_mirrors:
	  - "https://apache.osuosl.org/lucene/solr/"
	  - "https://archive.apache.org/dist/lucene/solr/"

Solr tar checksum and algorithm dynamically configured by default:

	solr_checksum: ""
	solr_checksum_algo: ""

User that runs solr and owns corresponding files and directories

	solr_user: solr

Starts and/or restarts solr service when true. Just installs solr when false:

	solr_deploy: true

Dictionary of key=>value pairs that populates `"{{ solr_dir }}"/bin/solr.in.sh`:

	solr_params:
	  SOLR_HOST: "{% for h in zk_hosts %}{% if h.host is defined %}{% if h.host == inventory_hostname %}{{ h.addr }}{% endif %}{% endif %}{% endfor %}"
	  SOLR_JAVA_HOME: /usr/lib/jvm/jre-1.8.0
	  SOLR_JAVA_MEM: "{% if ansible_facts['memory_mb']['swap']['total'] > ansible_facts['memory_mb']['real']['total'] %}\
	\"-Xms{{ (ansible_facts['memory_mb']['real']['total'] * 8)  // 20 }}m -Xmx{{ (ansible_facts['memory_mb']['real']['total'] * 8)  // 10 }}m\"\
	{% else %}\
	\"-Xms{{ (ansible_facts['memory_mb']['real']['total'] * 5)  // 20 }}m -Xmx{{ (ansible_facts['memory_mb']['real']['total'] * 5)  // 10 }}m\"\
	{% endif %}"
	  SOLR_PID_DIR: "{{ solr_data_dir }}"
	  SOLR_HOME: "{{ solr_data_dir }}/data"
	  LOG4J_PROPS: "{{ solr_data_dir }}/log4j.properties"
	  SOLR_LOGS_DIR: "{{ solr_data_dir }}/logs"
	  SOLR_PORT: 8983

Array of options that populates `GC_TUNE` in `solr.in.sh`:

	gc_tune:
	  - NewRatio=3
	  - SurvivorRatio=4
	  - TargetSurvivorRatio=90
	  - MaxTenuringThreshold=8
	  - +UseConcMarkSweepGC
	  - +UseParNewGC
	  - ConcGCThreads=4
	  - ParallelGCThreads=4
	  - +CMSScavengeBeforeRemark
	  - PretenureSizeThreshold=64m
	  - +UseCMSInitiatingOccupancyOnly
	  - CMSInitiatingOccupancyFraction=50
	  - CMSMaxAbortablePrecleanTime=6000
	  - +CMSParallelRemarkEnabled
	  - +ParallelRefProcEnabled

Array of options to pass to `SOLR_OPTS` in `solr.in.sh':`

	solr_opts:
	  - "-Xss256k"
	  - "-Djetty.host=$SOLR_HOST"

Dictionary of key=>value pairs that populate solr systemd unit:

	solr_systemd_params:
	  unit:
		 Description: Apache SOLR
		 After: syslog.target network.target remote-fs.target nss-lookup.target
	  service:
		 PIDFile: "{{ solr_data_dir }}/solr-8983.pid"
		 ExecStart: "/opt/solr/bin/solr start -noprompt"
		 ExecStop: "/opt/solr/bin/solr stop -noprompt"
		 # ExecStatus: "/opt/solr/bin/solr status -noprompt"
		 ExecReload: "/bin/kill -s HUP $MAINPID"
		 Environment: "SOLR_INCLUDE=/opt/solr/bin/solr.in.sh"
		 User: "solr"
		 Group: "solr"
		 PrivateTmp: "true"
	  install:
		 WantedBy: multi-user.target

Dependencies
------------

"geerlingguy.java" role must be installed


Example Playbook
----------------

```yaml
- hosts: zk-solr-servers
  roles:
    - tag1consulting.zk-solr
      zk_hosts:
        - host: "zk-solr1"
          addr: "10.0.1.111"
          id: 1
          leader_port: 2888
          election_port: 3888
          client_port: 2181
        - host: "zk-solr2"
          addr: "10.0.1.112"
          id: 2
          leader_port: 2888
          election_port: 3888
          client_port: 2181
        - host: "zk-solr3"
          addr: "10.0.1.113"
          id: 3
          leader_port: 2888
          election_port: 3888
          client_port: 2181
```

License
-------

BSD

Author Information
------------------

This role was created in 2020 by Kerry Vance, for [Tag1 Consulting](https://www.tag1consulting.com/)
