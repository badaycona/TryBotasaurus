import argparse
import asyncio
from scraper.cpu_scraper import scrape_cpus
from scraper.gpu_scraper import scrape_gpus
from scraper.ram_scraper import scrape_rams
from scraper.psu_scraper import scrape_psus
from scraper.motherboard_scraper import scrape_motherboards

PARTS = {
    'cpu': scrape_cpus,
    'gpu': scrape_gpus,
    'ram': scrape_rams,
    'psu': scrape_psus,
    'motherboard': scrape_motherboards,
}

def parse_args():
    parser = argparse.ArgumentParser(description='PCPartPicker Scraper')
    parser.add_argument('--cpu', action='store_true', help='Scrape CPUs')
    parser.add_argument('--gpu', action='store_true', help='Scrape GPUs')
    parser.add_argument('--ram', action='store_true', help='Scrape RAM')
    parser.add_argument('--psu', action='store_true', help='Scrape PSUs')
    parser.add_argument('--motherboard', action='store_true', help='Scrape Motherboards')
    parser.add_argument('--all', action='store_true', help='Scrape all parts')
    return parser.parse_args()

async def main():
    args = parse_args()
    tasks = []
    if args.all or not any([args.cpu, args.gpu, args.ram, args.psu, args.motherboard]):
        tasks = [func() for func in PARTS.values()]
    else:
        if args.cpu: tasks.append(scrape_cpus())
        if args.gpu: tasks.append(scrape_gpus())
        if args.ram: tasks.append(scrape_rams())
        if args.psu: tasks.append(scrape_psus())
        if args.motherboard: tasks.append(scrape_motherboards())
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
