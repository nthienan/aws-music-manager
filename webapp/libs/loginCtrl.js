/**
 * @author nthienan
 */
// login controller
mainApp.controller('loginCtrl', function ($rootScope, $scope, $http, $location, $cookieStore, ngProgress, $translate, langService, globalConfig) {
    $scope.rememberMe = false;
    $scope.haveError = false;

    $scope.showSignUp = function () {
        $location.path("/sign-up");
    }

    $scope.login = function () {
        ngProgress.start();
        $http({
            method: 'POST',
            url: globalConfig.baseURL + '/login',
            headers: {
                'Content-Type': 'application/json'
            },
            data: JSON.stringify({email: $scope.username, password: $scope.password})
        }).success(function (data, status) {
            var authToken = data.token;
            $scope.haveError = false;
            $rootScope.authToken = authToken;

            $cookieStore.put('authToken', authToken);
            $http.get(globalConfig.baseURL + '/user/me')
                .success(function (data) {
                    $rootScope.user = data;
                    $rootScope.authenticated = true;
                    ngProgress.complete();
                    $location.path("/");
                })
                .error(function (data, status) {
                    ngProgress.complete();
                });
        })
            .error(function (data, status) {
                $scope.haveError = true;
                $rootScope.error = "Username/password is incorect";
                ngProgress.complete();
            });
    };

    $scope.$on('langBroadcast', function () {
        $translate.use(langService.key);
        $scope.lang = langService.key;
    });
});