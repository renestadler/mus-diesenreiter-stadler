package at.fhooe.recyclingserver.logic;

import at.fhooe.recyclingserver.client.ProductClient;
import at.fhooe.recyclingserver.jpa.ProductRepository;
import at.fhooe.recyclingserver.jpa.RecyclingInfoRepository;
import at.fhooe.recyclingserver.model.Product;
import at.fhooe.recyclingserver.model.RecyclingInfo;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Optional;

import static java.util.Objects.requireNonNull;

@Service
public class ProductLogicImpl implements ProductLogic {

    private static final Logger LOG = LoggerFactory.getLogger(ProductLogicImpl.class);
    private final RecyclingInfoRepository recyclingInfoRepository;
    private final ProductRepository productRepository;
    private final ProductClient productClient;

    public ProductLogicImpl(RecyclingInfoRepository recyclingInfoRepository, ProductRepository productRepository,
                            ProductClient productClient) {
        this.recyclingInfoRepository = requireNonNull(recyclingInfoRepository);
        this.productRepository = requireNonNull(productRepository);
        this.productClient = requireNonNull(productClient);
    }

    @Override
    public Optional<Product> getProduct(String code) {
        Optional<Product> productByCode = productRepository.findProductByCode(code);
        if (productByCode.isPresent()) {
            productByCode.get().getPackagings().forEach(p -> p.setRecyclingInfo(recyclingInfoRepository.
                    findFirstByMaterial(p.getName())
                    .map(RecyclingInfo::getDisposalMethod).orElse("Unknown")));
            LOG.info("Retrieved Product from DB");
            return productByCode;
        }
        LOG.info("Retrieving Product from OpenFoodFacts");
        return productClient.getByCode(code).map(productRepository::save);
    }
}
