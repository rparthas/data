package ram.edu.twitterStorm.bolt;

import java.util.Calendar;
import java.util.Map;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Fields;
import org.apache.storm.tuple.Tuple;
import org.apache.storm.tuple.Values;

import ram.edu.twitterStorm.util.Util;

public class RollingCountBolt implements IRichBolt {

	public RollingCountBolt(long frequency) {
		this.frequency = frequency;
	}

	long start = 0;
	int count = 0;
	long frequency = 0;

	OutputCollector collector = null;

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		this.collector = collector;

	}

	public void execute(Tuple input) {
		String hashTag = input.getStringByField("hashTag");
		if (start == 0)
			start = Util.reset();
		if (hashTag != null) {
			count = count + 1;
		}
		if (Util.getDiff(start) > frequency) {
			start = Util.reset();
			collector.emit(new Values(hashTag, count));
			count = 0;
		}

	}

	public void cleanup() {
		// TODO Auto-generated method stub

	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("hashTag", "count"));

	}

	public Map<String, Object> getComponentConfiguration() {
		// TODO Auto-generated method stub
		return null;
	}

}
