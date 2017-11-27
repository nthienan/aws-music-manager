/**
 * @author nthienan
 */
// play controller
mainApp.controller('playCtrl', function ($rootScope, $scope, $http, $location, $routeParams, $window, ngProgress, $translate, langService, globalConfig) {
    $http.defaults.headers.post['Content-Type'] = 'application/json';

    // get a song by id to play
    $scope.load = function () {
        ngProgress.start();
        $http.get(globalConfig.baseURL + '/song/' + $routeParams.id)
            .success(function (res) {
                $scope.song = res;
            }).error(function (err) {
            ngProgress.complete();
        });
    };

    // download file
    $scope.downloadSong = function (path) {
        $window.open('/' + path, '_blank');
    };

    $scope.$on('langBroadcast', function () {
        $translate.use(langService.key);
        $scope.lang = langService.key;
    });

    // load data
    $scope.load();
});