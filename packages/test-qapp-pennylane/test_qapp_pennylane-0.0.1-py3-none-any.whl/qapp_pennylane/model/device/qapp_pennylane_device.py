"""
    QApp Platform Project
    qapp_pennylane_device.py
    Copyright © CITYNOW Co. Ltd. All rights reserved.
"""

import pennylane as qml
from qapp_common.data.response.authentication import Authentication
from qapp_common.data.response.project_header import ProjectHeader
from qapp_common.model.device.device import Device
from qapp_common.config.logging_config import logger
from qapp_common.data.device.circuit_running_option import CircuitRunningOption
from qapp_common.model.provider.provider import Provider
from qapp_common.enum.invocation_step import InvocationStep

from pennylane.tape import QuantumTape
import time


class QAppPennylaneDevice(Device):
  def __init__(self, provider: Provider, device_specification: str):
    super().__init__(provider, device_specification)
    logger.debug('[QAppPennylaneDevice] Initializing device specification')
    self.device_specification = device_specification

  def _create_job(self, circuit, options: CircuitRunningOption):
    logger.debug(
      '[QAppPennylaneDevice] Creating job with {0} shots'.format(options.shots))

    with QuantumTape() as tape:
      circuit()

    # pennylane job does not support returning the measurement, so we need to re-define the circuit to get the probabilities

    self.device = qml.device(self.device_specification, wires=tape.wires,
                             shots=options.shots)

    start_time = time.time()
    qnode = qml.QNode(circuit, self.device)
    job_result = qnode()
    end_time = time.time()

    histogram_index = qnode.tape.observables.index(qml.probs())
    result_histogram = {}
    for i, prob in enumerate(job_result[histogram_index]):
        bitstring = format(i, f'0{2}b')  # Convert index to bitstring
        result_histogram[bitstring] = int(prob*options.shots)

    data = {"result": job_result, "histogram": result_histogram, "time_taken_execute": end_time - start_time}

    return data

  def _is_simulator(self) -> bool:
    logger.debug('[QAppPennylaneDevice] Is simulator')
    return True

  def _produce_histogram_data(self, job_result) -> dict | None:
    logger.info('[PennylaneDevice] Producing histogram data')

    # try:
    #     histogram_data = job_result.get_counts()
    # except Exception as pennylane_error:
    #     logger.debug("[PennylaneDevice] Can't produce histogram with error: {0}".format(
    #         str(pennylane_error)))
    #     histogram_data = None

    # return histogram_data

    k = job_result.get('histogram')

    logger.debug(
      '[PennylaneDevice] Producing histogram data with {0}'.format(k))

    return job_result.get('histogram')

  def _get_provider_job_id(self, job) -> str:
    logger.debug('[PennylaneDevice] Getting job id')

    # no job id in local simulator
    return None

  def _get_job_status(self, job) -> str:
    logger.debug('[PennylaneDevice] Getting job status')

    return "DONE"

  def _get_job_result(self, job) -> dict:
    logger.debug('[PennylaneDevice] Getting job result')

    return job

  def _calculate_execution_time(self, job_result):
    logger.debug('[PennylaneDevice] Calculating execution time')

    self.execution_time = job_result.get('time_taken_execute')

    logger.debug('[PennylaneDevice] Execution time calculation was: {0} seconds'.format(self.execution_time))

  def run_circuit(self,
      circuit,
      post_processing_fn,
      options: CircuitRunningOption,
      callback_dict: dict,
      authentication: Authentication,
      project_header: ProjectHeader):
    """

    @param project_header: project header
    @param callback_dict: callback url dictionary
    @param options: Options for run circuit
    @param authentication: Authentication for calling quao server
    @param post_processing_fn: Post-processing function
    @param circuit: Circuit was run
    """

    original_job_result, job_response = self._on_execution(
        authentication=authentication,
        project_header=project_header,
        execution_callback=callback_dict.get(InvocationStep.EXECUTION),
        circuit=circuit,
        options=options)

    if original_job_result is None:
      return

    job_response = self._on_analysis(
        job_response=job_response,
        original_job_result=original_job_result,
        analysis_callback=callback_dict.get(InvocationStep.ANALYSIS))

    if job_response is None:
      return

    self._on_finalization(job_result=original_job_result.get('result'),
                           authentication=authentication,
                           post_processing_fn=post_processing_fn,
                           finalization_callback=callback_dict.get(
                             InvocationStep.FINALIZATION),
                           project_header=project_header)