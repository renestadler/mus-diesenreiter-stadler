package at.fhooe.recyclingserver.client;

import at.fhooe.recyclingserver.client.entity.PackagingDto;
import at.fhooe.recyclingserver.client.entity.PackagingResponseDto;
import at.fhooe.recyclingserver.client.entity.ProductPackagingDto;
import at.fhooe.recyclingserver.client.entity.ProductResponseDto;
import at.fhooe.recyclingserver.jpa.PackagingRepository;
import at.fhooe.recyclingserver.jpa.RecyclingInfoRepository;
import at.fhooe.recyclingserver.model.Packaging;
import at.fhooe.recyclingserver.model.Product;
import at.fhooe.recyclingserver.model.RecyclingInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import static java.util.Objects.requireNonNull;

@Component
public class OpenFoodFactsProductClient implements ProductClient {

    private static final Logger LOG = LoggerFactory.getLogger(OpenFoodFactsProductClient.class);
    private static final String BASE_URL = "https://de.openfoodfacts.org/";

    private final PackagingRepository packagingRepository;
    private final RecyclingInfoRepository recyclingInfoRepository;

    public OpenFoodFactsProductClient(PackagingRepository packagingRepository, RecyclingInfoRepository recyclingInfoRepository) {
        this.packagingRepository = requireNonNull(packagingRepository);
        this.recyclingInfoRepository = recyclingInfoRepository;
    }

    @Override
    public Optional<Product> getByCode(String code) {
        if (packagingRepository.count() == 0) {
            LOG.info("Retrieving Packagings");
            packagingRepository.saveAll(getPackagings());
        }
        LOG.info("Retrieving Product");
        Optional<Product> product = getProduct(code);
        LOG.info(product.toString());
        return product;

    }

    private List<Packaging> getPackagings() {
        RestTemplate restTemplate = new RestTemplate();
        PackagingResponseDto response = restTemplate.getForObject(BASE_URL + "verpackungen/1.json", PackagingResponseDto.class);
        assert response != null;
        List<Packaging> packagings = new ArrayList<>();
        for (PackagingDto packagingDto : response.getTags()) {
            if (packagingDto.getKnown() == 1) {
                packagings.add(new Packaging(
                        0,
                        packagingDto.getId(),
                        packagingDto.getName(),
                        true,
                        recyclingInfoRepository.findFirstByMaterial(packagingDto.getName())
                                .map(RecyclingInfo::getDisposalMethod)
                                .orElse("Unknown")
                ));
            }
        }
        return packagings;
    }

    private Optional<Product> getProduct(String code) {
        RestTemplate restTemplate = new RestTemplate();
        ProductResponseDto response = restTemplate.getForObject(BASE_URL + "api/v2/product/" + code + "?fields=packagings,generic_name,image_url", ProductResponseDto.class);
        assert response != null;
        if (response.getStatus() == 0 || response.getCode()==null) {
            return Optional.empty();
        }
        if(response.getProduct().getGeneric_name()==null){
            response.getProduct().setGeneric_name("");
        }
        if(response.getProduct().getImage_url()==null){
            response.getProduct().setImage_url("");
        }
        List<Packaging> packagings = new ArrayList<>();
        for (ProductPackagingDto packagingDto : response.getProduct().getPackagings()) {
            packagingRepository.findPackagingByCode(packagingDto.getMaterial()).ifPresent(packagings::add);
        }
        return Optional.of(
                new Product(
                        0,
                        response.getCode(),
                        response.getProduct().getGeneric_name(),
                        response.getProduct().getImage_url(),
                        packagings
                )
        );
    }
}
