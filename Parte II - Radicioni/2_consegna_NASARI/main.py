import os
from prettytable import PrettyTable
from summary import *
from metrics import *


if __name__ == "__main__":

    documents = ['Andy-Warhol.txt', 'Ebola-virus-disease.txt', 'Life-indoors.txt', 'Napoleon-wiki.txt', 'Trump-wall.txt']
    reductions = [10,20,30]

    #parsifico i vettori di nasari in un dizionario
    nasari_parsed = parse_nasari_vectors()

    resultTable = PrettyTable(["/","Blue 10%","Rouge 10%","Blue 20%","Rouge 20%","Blue 30%","Rouge 30%"])

    for document in documents:

        #parsifico il documento
        parsed_document = parse_document(document)

        #ricavo il riassunto
        summary_10,summary_20,summary_30 = summarization(parsed_document, nasari_parsed, reductions)

        percentage = reductions[0]
        value_metrics = []

        for summary in [summary_10,summary_20,summary_30]:

            # Misuro le performance della summarizzation
            blue = blue_metric(parsed_document, summary)
            rouge = rouge_metric(parsed_document, summary)

            value_metrics.append(blue)
            value_metrics.append(rouge)

            #scrivo il riassunto sul file
            output_file_path = r".\output\\" + str(percentage) + '_' + document
            if os.path.exists(output_file_path):
                os.remove(output_file_path)

            output = open(output_file_path, 'a', encoding='utf-8')
            for paragraph in summary:
                output.write(paragraph)
                output.write("\n")
            output.close()
            percentage+=10

        resultTable.add_row([document]+value_metrics)
    print(resultTable)
