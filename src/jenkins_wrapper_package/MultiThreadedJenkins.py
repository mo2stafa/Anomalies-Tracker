from src.jenkins_wrapper_package.JenkinsWrapper import JenkinsWrapper
import threading
import logging
import os


log_folder = os.path.join(os.path.dirname(__file__),'..','..', 'logs')
os.makedirs(log_folder, exist_ok=True)

log_file = os.path.join(log_folder, 'info.log')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)


logger = logging.getLogger(__name__)



class MultiThreadedJenkins:
    def __init__(self, url: str, username: str, password: str):
        self.jenkins_wrapper = JenkinsWrapper(url, username, password)
        self.finished_jobs = []


    def job_thread(self,job_name, xml_config):
        try:
            self.jenkins_wrapper.create_job_from_xml(job_name, xml_config)

            build_info = self.jenkins_wrapper.build_job(job_name)

            self.jenkins_wrapper.wait_for_job_creation(job_name)

            build_number = self.jenkins_wrapper.wait_for_job_to_start_building(job_name)
            
            # thread_fetch_output = threading.Thread(target=self.jenkins_wrapper.fetch_and_update_console_output,
            #                                         args=(job_name, build_number))
            # thread_fetch_output.start()

            # thread_fetch_output.join()

            self.jenkins_wrapper.wait_for_job_to_finish_building(job_name, build_number)

            job_status = self.jenkins_wrapper.get_build_status(job_name, build_number)
            job_execution_time = self.jenkins_wrapper.get_execution_time(job_name, build_number)
            self.finished_jobs.append((job_name, job_status, job_execution_time))

            message = f"Job '{job_name}' finished with status: {job_status}  , execution time: {job_execution_time}"
            logger.info(message) 
            print(message)
            self.jenkins_wrapper.delete_job(job_name)
        except Exception as e:
            message =f"Exception occurred for job '{job_name}': {e}"
            logger.error(message) 
            print(message)
            self.jenkins_wrapper.delete_job(job_name)