import apache_beam as beam
from apache_beam.io import WriteToText
import logging

class SplitWords(beam.DoFn):
  def process(self, element):
     
     results = []
     words = element.split()
     
     for word in words:
        results.append((word, 1))
     
     return results
           
def run():
     PROJECT_ID = 'your-project' # change to your project id

     options = {
     'project': PROJECT_ID
     }
     opts = beam.pipeline.PipelineOptions(flags=[], **options)

     p = beam.Pipeline('DirectRunner', options=opts)

     in_pcoll = p | beam.Create(['here are some words', 'here a few more words'])

     split_pcoll = in_pcoll | 'Split Words' >> beam.ParDo(SplitWords())
     
     grouped_pcoll = split_pcoll | 'Group Words' >> beam.GroupByKey()
        
     grouped_pcoll | 'Write results' >> WriteToText('grouped.txt')
    
     result = p.run()
     result.wait_until_finish() 

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.ERROR)
  run()
