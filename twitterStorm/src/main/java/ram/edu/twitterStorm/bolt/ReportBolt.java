package ram.edu.twitterStorm.bolt;

import org.apache.storm.task.OutputCollector;
import org.apache.storm.task.TopologyContext;
import org.apache.storm.topology.IRichBolt;
import org.apache.storm.topology.OutputFieldsDeclarer;
import org.apache.storm.tuple.Tuple;

import java.util.Map;

/**
 * Created by ram on 7/05/16.
 */
public class ReportBolt implements IRichBolt {

	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {

	}

	public void execute(Tuple input) {
		System.out.println(input.getStringByField("hashTag"));
	}

	public void cleanup() {

	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {

	}

	public Map<String, Object> getComponentConfiguration() {
		return null;
	}
}
