import datetime, logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import WriteToText
from apache_beam.io.gcp.bigquery import ReadFromBigQuery, WriteToBigQuery

class FormatName(beam.DoFn):
  def process(self, element):
    tid = element['tid']
    instructor = element['instructor']
    dept = element['dept']

    split_name = instructor.split(',')
    if len(split_name) > 1:
        lname = split_name[0]
        fname = split_name[1]
    else:
        split_name = instructor.split(' ')
        fname = split_name[0]
        lname = split_name[1]
        
    record = {'tid': tid, 'fname': fname, 'lname': lname, 'dept': dept}
    return [record]
           
def run():
     PROJECT_ID = 'my-project' 
     BUCKET = 'gs://my-bucket' 
     DIR_PATH = BUCKET + '/output/' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '/'

     options = PipelineOptions(
     flags=None,
     runner='DataflowRunner',
     project=PROJECT_ID,
     job_name='teacher',
     temp_location=BUCKET + '/temp',
     region='us-central1')

     p = beam.pipeline.Pipeline(options=options)

     sql = 'SELECT tid, instructor, dept FROM college_staging.Teacher'
     bq_source = ReadFromBigQuery(query=sql, use_standard_sql=True, gcs_location=BUCKET)

     query_results = p | 'Read from BQ' >> beam.io.Read(bq_source)

     out_pcoll = query_results | 'Format Name' >> beam.ParDo(FormatName())

     out_pcoll | 'Log output' >> WriteToText(DIR_PATH + 'output.txt')

     dataset_id = 'college_refined'
     table_id = PROJECT_ID + ':' + dataset_id + '.' + 'Teacher_Dataflow'
     schema_id = 'tid:STRING,fname:STRING,lname:STRING,dept:STRING'

     out_pcoll | 'Write to BQ' >> WriteToBigQuery(table=table_id, schema=schema_id, custom_gcs_temp_location=BUCKET)
     
     result = p.run()
     result.wait_until_finish()      


if __name__ == '__main__':
  logging.getLogger().setLevel(logging.ERROR)
  run()