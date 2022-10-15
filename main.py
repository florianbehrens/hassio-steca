import aiohttp
import asyncio
import untangle

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://steca/measurements.xml') as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html)
            
            document = untangle.parse(html)
            print("Untangled:", document)
            print("Device name: ", document.root.Device["Name"])
            
            #for measurement in document.root.Device.Measurements.Measurement:
            #    print(measurement["Type"], " = ", measurement["Value"], " ", measurement["Unit"])

            #print({ measurement["Type"]:(measurement["Value"], measurement["Unit"]) for (measurement) in document.root.Device.Measurements.Measurement })

            new_dict = {}
            for item in document.root.Device.Measurements.Measurement:
                new_dict[item['Type']] = (
                    item['Value'] if item['Value'] else 0,
                    item['Unit']
                )
            
            print(new_dict)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
