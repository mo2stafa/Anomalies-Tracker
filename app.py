import threading

from src.jenkins_wrapper_package.MultiThreadedJenkins import MultiThreadedJenkins



def main():
    multi_jenkins = MultiThreadedJenkins('http://localhost:8080/', 'admin', '11f6ffd591aa58166016b94c900f0c361d')

    jobs_to_execute = ['job_1', 'job_2', 'job_3']
    xml_configs = [
        """<?xml version="1.0" encoding="UTF-8"?><project><actions/><description>Description</description><keepDependencies>false</keepDependencies><properties/><scm class="hudson.scm.NullSCM"/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.tasks.BatchFile><command>python "C:/Users/moham/Desktop/Anomalies Tracker/resources/scripts/script1.py"</command><configuredLocalRules/></hudson.tasks.BatchFile></builders><publishers/><buildWrappers/></project>""",
        """<?xml version="1.0" encoding="UTF-8"?><project><actions/><description>Description</description><keepDependencies>false</keepDependencies><properties/><scm class="hudson.scm.NullSCM"/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.tasks.BatchFile><command>python "C:/Users/moham/Desktop/Anomalies Tracker/resources/scripts/script2.py"</command><configuredLocalRules/></hudson.tasks.BatchFile></builders><publishers/><buildWrappers/></project>""",
        """<?xml version="1.0" encoding="UTF-8"?><project><actions/><description>Description</description><keepDependencies>false</keepDependencies><properties/><scm class="hudson.scm.NullSCM"/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.tasks.BatchFile><command>python "C:/Users/moham/Desktop/Anomalies Tracker/resources/scripts/script3.py"</command><configuredLocalRules/></hudson.tasks.BatchFile></builders><publishers/><buildWrappers/></project>"""
    ]



    jobs_to_execute = [f'job_{i}' for i in range(1, 6)]
    new_xml_configs = xml_configs * ((5 + len(xml_configs) - 1) // len(xml_configs))
    




    threads = []
    for job_name, xml_config in zip(jobs_to_execute, new_xml_configs):
        t = threading.Thread(target=multi_jenkins.job_thread, args=(job_name, xml_config))
        threads.append(t)
        t.start()


    # time.sleep(30)
    # build_number = multi_jenkins.jenkins_wrapper.get_last_build_number("job_1")
    # multi_jenkins.jenkins_wrapper.abort_build("job_1",build_number)


    for t in threads:
        t.join()


    for job, status, time in multi_jenkins.finished_jobs:
        print(f"Job '{job}' finished with status: {status}  , build time: {time}")

if __name__ == "__main__":
    main()
