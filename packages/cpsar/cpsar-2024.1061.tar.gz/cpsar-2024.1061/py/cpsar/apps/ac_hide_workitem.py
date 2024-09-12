import cpsar.runtime as R
import cpsar.wsgirun as W
from cpsar.workqueue import WorkQueue

@W.wsgi
@W.json
def application(req, res):
    job_class = req.params.get('job_class')
    gn = req.params.get('group_number')
    ga = req.params.get('group_auth')

    if not (job_class and gn and ga):
        res.error("Invalid parameter")
        return
    WorkQueue.hide(job_class, gn, ga)
    R.db.commit()
