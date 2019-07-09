(function () {
    'use strict';
    angular.module("isyplus")

    .config(config);
    function config($stateProvider){
        $stateProvider.state('upload', {
            url : '/upload/',
            templateUrl: 'static/app/uploadfile/upload.html?v=' + globalgsvapp,
            controller: 'UploadCntrl'
        });
    }

})();



