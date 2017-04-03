package ram.edu.twitterStorm.bolt;

import java.util.Map;
import java.util.Set;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import ram.edu.twitterStorm.util.RedisClient;
import ram.edu.twitterStorm.util.Util;
import redis.clients.jedis.Jedis;

public class CountBolt implements IRichBolt {

	long start=0;
	public CountBolt() {

	}

	OutputCollector collector = null;

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		this.collector = collector;

	}

	public void execute(Tuple input) {
		String hashTag = input.getStringByField("hashTag");
		Double count = RedisClient.get(hashTag);
		if (count == null) {
			count = 0.0;
		}
		count = count + 1;

		RedisClient.put(hashTag, count);
		if(start == 0)
		start=Util.reset();
		if(Util.getDiff(start) > 20000){
			start=Util.reset();
			Set<String> hashTags = RedisClient.rank();
			for (String tag : hashTags) {
				System.out.println(tag);
			}
		}
	}

	public void cleanup() {
		// TODO Auto-generated method stub

	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		
	}

	public Map<String, Object> getComponentConfiguration() {
		// TODO Auto-generated method stub
		return null;
	}

}
