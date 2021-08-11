import csv

def group():
    print("--------Start---------")
    with open("TIM_LLC_CORP.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 1

        for row in csv_reader:
            print("Count-----------------> : ", line_count)

            if line_count == 1:
                print("read header")
            
            if line_count > 1:
                county         = row[0]
                parcel         = row[1]
                buyer_first    = row[2]
                buyer_last     = row[3]
                mail_addr      = row[4]
                mail_city      = row[5]
                mail_state     = row[6]
                mail_zip       = row[7]
                mail_cntry     = row[8]
                sale_date      = row[9]
                sale_price     = row[10]
                legal_class    = row[11]
                legal_subclass = row[12]
                prop_addr      = row[13]      
                prop_city      = row[14]
                prop_state     = row[15]
                prop_zip       = row[16]
                sqr_ft         = row[17]
                con_year       = row[18]
                prop_use       = row[19]
                sr_entity_name = row[20]
                sr_name        = row[21]
                sr_maddress    = row[22]


                gp_entity_count = 0
                gp_name_count = 0
                sr_entity_name = ''.join(sr_entity_name).strip() if sr_entity_name else ""
                sr_name = ''.join(sr_name).strip() if sr_name else ""
                
                gp_entity = ""
                gp_name = ""

                print(sr_entity_name)
                print(sr_name)


                with open("TIM_LLC_CORP.csv") as csv_file1:
                    csv_reader1 = csv.reader(csv_file1, delimiter=",")

                    for row1 in csv_reader1:
                        entity_name = row1[20]
                        name        = row1[21]

                        entity_name = ''.join(entity_name).strip() if entity_name else ""
                        name = ''.join(name).strip() if name else ""

                        if sr_entity_name != "":
                            if sr_entity_name == entity_name:
                                gp_entity_count += 1
                        else: 
                            gp_entity_count = 0

                        if sr_name != "": 
                            if sr_name == name:
                                gp_name_count += 1
                        else:
                            gp_name_count = 0

                    if gp_entity_count == 0:
                        gp_entity = ""
                    if gp_entity_count > 0 and gp_entity_count < 3:
                        gp_entity = "1--2"
                    elif gp_entity_count > 2 and gp_entity_count < 6:
                        gp_entity = "3--5"
                    elif gp_entity_count > 5 and gp_entity_count < 11:
                        gp_entity = "6--10"
                    elif gp_entity_count > 10 and gp_entity_count < 20:
                        gp_entity = "11--20"
                    elif gp_entity_count > 19:
                        gp_entity = "20+"

                    if gp_name_count == 0:
                        gp_name = ""
                    if gp_name_count > 0 and gp_name_count < 3:
                        gp_name = "1--2"
                    elif gp_name_count > 2 and gp_name_count < 6:
                        gp_name = "3--5"
                    elif gp_name_count > 5 and gp_name_count < 11:
                        gp_name = "6--10"
                    elif gp_name_count > 10 and gp_name_count < 20:
                        gp_name = "11--20"
                    elif gp_name_count > 19:
                        gp_name = "20+"


                print("Entity Count----------------> : ", gp_entity_count)
                print("Name Count------------------> : ", gp_name_count)

                with open("TIM_LLC_CORP_GROUP.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)

                    writer.writerow([county, parcel, buyer_first, buyer_last, mail_addr, mail_city, mail_state, mail_zip, mail_cntry, sale_date, sale_price, legal_class, legal_subclass, prop_addr, prop_city, prop_state, prop_zip, sqr_ft, con_year, prop_use, sr_entity_name, sr_name, sr_maddress, gp_entity, gp_name])

            line_count += 1

if __name__ == "__main__":
    open("TIM_LLC_CORP_GROUP.csv", "wb").close()
    header = ["County", "Parcel", "BuyerFirst", "BuyerLast", "MailAddr", "MailCity", "MailState", "MailZip", "MailCntry", "SaleDate", "SalePrice", "LegalClass", "LegalSubClass", "PropAddr", "PropCity", "PropState", "PropZip", "SqrFt", "ConstructionYear", "PropUse", "County", "SrEntityName", "SrName", "SrMAddress", "Grouped_Entity", "Grouped_Name"]


    with open("TIM_LLC_CORP_GROUP.csv", "a", newline="") as f:
        csv_writer = csv.DictWriter(f, fieldnames=header, lineterminator='\n')
        csv_writer.writeheader()

    group()