angular.module('a3app.controllers', [])
.controller('globalCtrl', function($scope, $rootScope, $http) {
  $scope.inSession = false;
  $rootScope.inSession = $scope.inSession;
  if(window.innerWidth < 768)
    $scope.isCollapsed = true;
  else
    $scope.isCollapsed = false;

  $scope.a3file = null; // data about uploaded file
  $scope.demoProp = 'demo';

  $scope.showSidebar = function(yes) {
    $scope.inSession = yes;
  }
})
.controller('loginCtrl', function($scope, $http, $state) {
  $scope.showSidebar(false);

  $scope.try_login = function() {
    if($scope.loginform.$valid) {
      $http.post('/api/login', {
        email: $scope.email,
        passwd: $scope.passwd
      }).success(function(res) {
        console.log('LOGIN SUCCESS', res);
        if(res.status == 'success') {
          $state.go('app.cleanup');
        } else {
          $scope.email = 'Wrong Credentials';
          $scope.passwd = ''
        }
      });
    }
  };
})
.controller('signupCtrl', function($scope) {
  $scope.showSidebar(false);
})
.controller('plotCtrl', function($scope) {
  $scope.showSidebar(true);
  $scope.imageUrl = '';
  $scope.imageType = null;

  $scope.plotImage = function(imageType) {
    if($scope.imageType != imageType) {
      // $http.get() TODO
    }
  }
})
.controller('cleanupCtrl', function($scope, $http) {
  $scope.showSidebar(true);

  $scope.operations = [
  {'name':'misssing value', 'para':['cols','replace_by']},
  {'name':'replace value', 'para':['col', 'to_replace', 'replace_by']},
  {'name':'replace non number', 'para':['cols','replace_by','to_int']},
  {'name':'replace negative', 'para':['col','delete','replace_by']},
  {'name':'to upper', 'para':['col']},
  {'name':'to lower', 'para':['col']}
  ];

  $scope.selectedOperation = 0;
});