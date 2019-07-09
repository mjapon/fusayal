(function () {
    'use strict';
    angular.module("isyplus")
        .factory("AutorizacionServ", AutorizacionServ);

    function AutorizacionServ($resource) {
        return $resource("/rest/autorizacion/:aut_id",
            {aut_id: '@aut_id'}, {
                getForm: {
                    method: 'GET',
                    params: {
                        accion: 'form'
                    }
                },
                /*
                Se debe pasar el parametro cnt_id
                 */
                getContribAuts : {
                    method: 'GET',
                    params: {
                        accion: 'contribauts'
                    }
                }
            });
    }
})();