package choyware.cwserver;

import org.restlet.*;
import org.restlet.data.*;
import org.restlet.routing.*;
import java.util.logging.*;


public class CWServerApp extends Application {

	Component _component;
	Router _router;
	
	public static int globalPort = 8888;  // define access port 8888 (protect via nginx)
	
	public CWServerApp()
	{
		_component = new Component();
		_router = new Router(getContext());
		
		init();
	}
	
	private Component getComponent() { return _component; }
	private Router getRouter() { return _router; }
	
	@Override
	public synchronized Restlet createInboundRoot()
	{
		return getRouter();
	}
	
	private void setupLogging()
	{
		Logger logger = Logger.getLogger("org.restlet");
		for (Handler handler : logger.getParent().getHandlers())
		{
			if (handler.getClass().equals(java.util.logging.ConsoleHandler.class))
				handler.setLevel(Level.INFO);
		}
	}
	
	private void addProtocol(Component c, Protocol protocol, int port)
	{
		System.out.println("Listening on localhost:" + port + " protocol:" + protocol.getName());
		c.getServers().add(protocol, port);
	}
	
	private void setupBindings()
	{
		
	}
	
	/**
	 *  All important initialization for this app
	 */
	private void init()
	{
		setupLogging();
		
		addProtocol(getComponent(), Protocol.HTTP, globalPort);
		
		setupBindings();
	}
	
	public static void main(String[] args) {

	}

}
