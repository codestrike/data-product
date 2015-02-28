angular.module('a3app.controllers', [])
.controller('globalCtrl', function($scope, $http) {
  $scope.isSession = false;
  if(window.innerWidth < 768)
    $scope.isCollapsed = true;
  else
    $scope.isCollapsed = false;
  console.log($scope.isCollapsed, $scope.isSession);

  $scope.a3file = null; // data about uploaded file
  $scope.demoProp = 'demo';
})
.controller('loginCtrl', function($scope, $http, $state) {
  $scope.isSession = false;

  $scope.try_login = function() {
    console.log($scope.email);
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
  $scope.isSession = false;
  console.log('in signupCtrl now!');
})
.controller('plotCtrl', function($scope) {
  $scope.isSession = true;
  $scope.imageUrl = '';
  $scope.imageType = null;

  $scope.plotImage = function(imageType) {
    if($scope.imageType != imageType) {
      // $http.get() TODO
    }
  }
})
.controller('cleanupCtrl', function($scope, $http) {
  $scope.isSession = true;

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