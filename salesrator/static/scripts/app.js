window.a3app = angular.module('Salesrator', ['ui.router', 'ui.bootstrap', 'a3app.controllers']);

window.a3app.config(function($stateProvider, $urlRouterProvider) {
  // Setup routes
  $stateProvider
  .state('app', {
    abstract: true,
    url: '/app',
    template: '<div><div ui-view></div></div>',
    controller: 'globalCtrl'
  })
  .state('app.cleanup', {
    url: '/cleanup',
    templateUrl: '/static/part/cleanup.html',
    controller: 'cleanupCtrl'
  })
  .state('app.plot', {
    url: '/plot',
    templateUrl: '/static/part/plot.html',
    controller: 'plotCtrl'
  });
  // Default redirect
  $urlRouterProvider.otherwise('/app/cleanup');
});