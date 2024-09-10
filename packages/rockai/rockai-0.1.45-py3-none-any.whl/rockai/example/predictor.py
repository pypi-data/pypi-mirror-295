from rockai import (
    BasePredictor,
    Input,
    thread_limit
)
import logging

class Predictor(BasePredictor):

    def setup(self):
        #setup your model here
        self.logger = logging.getLogger()
        self.logger.setLevel("DEBUG")
        self.logger.debug("")

    #limit the number of threads runnig, the more threads the more GRAM it will be used when doing predictions
    @thread_limit(1)
    def predict(
        self, name: int = Input(description="stream total number of words")
    ) -> str:
        #start prediction
        self.logger.debug("predicting...")
        
        #return your result here
        return f"Hello, {name}"
