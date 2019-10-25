exports = {

  events: [
    { event: 'onAppInstall', callback: 'onInstallHandler' },
    { event: 'onTicketCreate', callback: 'onTicketCreateHandler' },
    { event: "onExternalEvent", callback: "onExternalEventHandler" }
  ],

  onInstallHandler: function (args) {
    generateTargetUrl().done(function (targetUrl) {
      console.log(targetUrl);
    });
  },

  // args is a JSON block containing the payload information.
  // args['iparam'] will contain the installation parameter values.
  onTicketCreateHandler: function(args) {
    console.log('Hello ' + args['data']['requester']['name']);
  },

  onExternalEventHandler: function(args) {
    console.log("Logging arguments from onExternalEvent: " +  JSON.stringify(args));
    //your code to perform action within freshdesk
  }
};
