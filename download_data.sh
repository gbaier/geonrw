#!/bin/bash

# List of the largest cities in NRW
# https://en.wikipedia.org/wiki/List_of_cities_in_North_Rhine-Westphalia_by_population

URLS=(
    # dop are RGB photos of 0.1m resolution
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05334002_Aachen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05378004_Bergisch_Gladbach_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05711000_Bielefeld_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05911000_Bochum_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05314000_Bonn_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05554012_Borken_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05512000_Bottrop_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05558012_Coesfeld_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05913000_Dortmund_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05112000_Duisburg_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05358008_Düren_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05111000_Düsseldorf_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05954008_Ennepetal_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05362020_Erftstadt_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05366016_Euskirchen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05113000_Essen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05513000_Gelsenkirchen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05754008_Gütersloh_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05914000_Hagen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05915000_Hamm_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05916000_Herne_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05370016_Heinsberg_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05758012_Herford_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05762020_Höxter_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05154036_Kleve_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05315000_Köln_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05114000_Krefeld_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05316000_Leverkusen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05974024_Lippetal_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05974028_Lippstadt_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05566048_Lotte_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05170024_Moers_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05116000_Mönchengladbach_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05117000_Mülheim_an_der_Ruhr_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05515000_Münster_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05162024_Neuss_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05119000_Oberhausen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05774032_Paderborn_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05562032_Recklinghausen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05120000_Remscheid_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05970040_Siegen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05122000_Solingen_EPSG25832_JPEG2000.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/lbi/dop/dop_jp2_f10_paketiert/dop_05124000_Wuppertal_EPSG25832_JPEG2000.zip

    # 3dm are LIDAR point clouds with roughly 4 points per square meter
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05334002_Aachen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05378004_Bergisch_Gladbach_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05711000_Bielefeld_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05911000_Bochum_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05314000_Bonn_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05554012_Borken_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05512000_Bottrop_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05558012_Coesfeld_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05913000_Dortmund_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05112000_Duisburg_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05358008_Düren_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05111000_Düsseldorf_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05954008_Ennepetal_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05362020_Erftstadt_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05366016_Euskirchen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05113000_Essen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05513000_Gelsenkirchen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05754008_Gütersloh_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05914000_Hagen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05915000_Hamm_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05916000_Herne_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05370016_Heinsberg_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05758012_Herford_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05762020_Höxter_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05154036_Kleve_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05315000_Köln_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05114000_Krefeld_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05316000_Leverkusen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05974024_Lippetal_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05974028_Lippstadt_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05566048_Lotte_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05170024_Moers_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05116000_Mönchengladbach_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05117000_Mülheim_an_der_Ruhr_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05515000_Münster_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05162024_Neuss_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05119000_Oberhausen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05774032_Paderborn_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05562032_Recklinghausen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05120000_Remscheid_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05970040_Siegen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05122000_Solingen_EPSG25832.zip
    https://www.opengeodata.nrw.de/produkte/geobasis/hm/3dm_l_las/3dm_l_las_paketiert/3dm_l_las_05124000_Wuppertal_EPSG25832.zip
)

DOWNLOAD_DIR=/data/ggeoinfo/datasets/nrw/download

mkdir $DOWNLOAD_DIR
cd $DOWNLOAD_DIR

for url in ${URLS[@]}; do
    file=${url##*/}
    if [ -f $file ]; then
        echo "$file already downloaded. Skipping."
    else
        echo "Starting download of $file"
        wget -c $url
    fi
done
