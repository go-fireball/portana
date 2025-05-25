@echo off

poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\msft_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\amzn_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\tpl_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\goog_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\aapl_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\meta_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_1_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_2_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_3_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_4_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_5_1290.csv ^
&& poetry run python -m app import --broker schwab --format lot_details --email venkatachalapatee@gmail.com --account 1290 --file .\temp_data\nvda_6_1290.csv

