(function () {
    'use strict';
    angular.module("isyplus")
        .factory("JobService", JobService);

    function JobService($resource) {
        return $resource("/rest/job/:job_id",
            {job_id: '@job_id'}, {
                getForm: {
                    method: 'GET',
                    params: {
                        accion: 'form'
                    }
                },
                cambiarEstado: {
                    method: 'POST',
                    params: {
                        accion: 'cambiar_estado'
                    }
                }
            });
    }

})();