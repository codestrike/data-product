window.a3app = angular.module('Salesrator', ['ui.router', 'ui.bootstrap', 'a3app.controllers']);

window.a3app.config(function($stateProvider, $urlRouterProvider) {
  // Setup routes
  $stateProvider
  .state('app', {
    abstract: true,
    url: '/app',
    templateUrl: '/static/part/menu.html',
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
  })
  .state('app.dash', {
    url: '/dash',
    templateUrl: '/static/part/dash.html',
    controller: 'dashCtrl'
  })
  .state('app.signup', {
    url: '/signup',
    templateUrl: '/static/part/signup.html',
    controller: 'signupCtrl'
  })
  .state('app.login', {
    url: '/login',
    templateUrl: '/static/part/login.html',
    controller: 'loginCtrl'
  });

  // Default redirect
  $urlRouterProvider.otherwise('/app/login');
});