total_belanja =int(input ("Total belanja: Rp"))
bayar = total_belanja
if total_belanja > 100000:
    print("kamu mendapatkan bonus minuman dan diskon 5%")
    
    diskon = total_belanja * 5/100
    bayar = total_belanja - diskon

    print("Total yang harus dibayar :Rp %s" % bayar)
else :
    print("Terimakasih sudah berbelanja Datang lagi ya")
