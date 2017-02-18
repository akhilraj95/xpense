from fpdf import FPDF, HTMLMixin
from .. import models
import actions
import flockappsecret as secret

class MyFPDF(FPDF, HTMLMixin):
    pass



def generate_report(trk,usr):
    html = """
    <h3 align="center">Expense Report</h3>
    <h3>Employee Expense Report</h3>
    <table border="0" width="90%" align="center">
    <thead>
    <tr><th width="30%">Name</th><th width="10%">Division</th><th width="10%">Depatment</th><th width="30%">Location</th><th width="20%">Travelling allowance</th></tr>
    </thead>
    <tbody>
    <tr>
    <td>"""+usr.name+"""</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    <td>{}</td>
    </tr>
    </tbody>
    </table>
    <p><strong>Business Pupose Visit:</strong></p>
    <p>Insert the purpose of the visit</p>
    <table border="0" width="90%" align="center">
    <thead>
    <tr><th width="20%">employee</th><th width="30%">pupose</th><th width="10%">time</th><th width="20%">date</th><th width="10%">cost</th></tr>
    </thead>
    <tbody>"""
    cur_qs = models.Currency.objects.all()
    total_dic = {}
    for cur in cur_qs:
        ex_qs = models.Expense.objects.filter(track = trk,currency=cur)
        sum = 0.0
        for ex in ex_qs:
            tm = ex.timestamp.time()
            sum = sum + ex.amount
            html = html +"""<tr><td>"""+ex.paidby.name+"""</td><td>"""+ex.purpose+"""</td><td>"""+str(tm.hour)+':'+str(tm.minute)+"""</td><td>"""+str(ex.timestamp.date())+"""</td><td>"""+ex.currency.abbr+' '+str(ex.amount)+"""</td></tr>"""
        if(sum!=0):
            total_dic[cur.name] = str(sum)
    for curr,val in total_dic.iteritems():
        html = html +"""<tr><td></td><td></td><td></td><td><b>Total cost</b></td><td>"""+curr+' '+str(val)+"""</td></tr>"""

    html = html + """
    </tbody>
    </table>
    <hr>
    <p>I hereby certify, to the best of my knowledge and belief, that (1) all information contained on this report is correct and (2) all expenses claimed on this report are based on actual costs incurred and are consistent with Company/Operations/Division procedures and the instructions on the reverse side of this form.</p>
    <p>Employee signature:___________________</p>s
    """
    pdf=MyFPDF()
    pdf.add_page()
    pdf.write_html(html)
    pdf.output('media/'+usr.userId+'.pdf','F')
    actions.bot_sendMessage(usr.userId,'<a>'+secret.get_url()+'/media/'+usr.userId+'.pdf'+'</a>')
    return
