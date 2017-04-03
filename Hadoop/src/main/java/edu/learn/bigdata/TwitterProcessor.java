package edu.learn.bigdata;

import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.SequenceFileInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class TwitterProcessor
		implements Mapper<LongWritable, Text, Text, IntWritable>, Reducer<Text, IntWritable, Text, IntWritable> {

	public static void main(String[] args) throws Exception {
		JobConf conf = new JobConf(TwitterProcessor.class);
		conf.setJobName("hashTagCount");
		conf.setMapperClass(TwitterProcessor.class);
		conf.setCombinerClass(TwitterProcessor.class);
		conf.setReducerClass(TwitterProcessor.class);

		conf.setInputFormat(SequenceFileInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(IntWritable.class);

		FileInputFormat.setInputPaths(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));

		JobClient.runJob(conf);

	}

	@Override
	public void configure(JobConf job) {

	}

	@Override
	public void close() throws IOException {

	}

	@Override
	public void map(LongWritable key, Text value, OutputCollector<Text, IntWritable> output, Reporter reporter)
			throws IOException {

		output.collect(new Text(value.getBytes()), new IntWritable(1));
	}

	@Override
	public void reduce(Text key, Iterator<IntWritable> values, OutputCollector<Text, IntWritable> output,
			Reporter reporter) throws IOException {
		int sum = 0;
		while (values.hasNext()) {
			sum += values.next().get();
		}
		output.collect(key, new IntWritable(sum));
	}

}
